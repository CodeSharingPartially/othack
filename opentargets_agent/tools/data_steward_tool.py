import requests
from typing import List, Dict

def get_disease_targets(
    disease_id: str,
    limit: int = 10,
    return_ensembl_ids: bool = True
) -> List[str]:
    """
    Query Open Targets GraphQL API for targets associated with a disease.

    Args:
        disease_id: Disease identifier (e.g., 'MONDO_0004979' for asthma)
        limit: Maximum number of results to return
        return_ensembl_ids: If True, return Ensembl IDs (default); if False, return gene symbols

    Returns:
        List of target identifiers (Ensembl IDs or gene symbols) associated with the disease
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"
    
    query = """
    query DiseaseTargets($diseaseId: String!, $limit: Int!) {
      disease(efoId: $diseaseId) {
        id
        name
        associatedTargets(
          page: { index: 0, size: $limit }
        ) {
          count
          rows {
            target {
              id
              approvedSymbol
              approvedName
              biotype
            }
            score
            datatypeScores {
              id
              score
            }
          }
        }
      }
    }
    """
    
    variables = {
        "diseaseId": disease_id,
        "limit": limit
    }
    
    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )

    # Print response details for debugging
    #print(f"Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")

    response.raise_for_status()

    data = response.json()
    
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    disease_data = data["data"]["disease"]
    if disease_data is None:
        raise Exception(f"Disease with ID '{disease_id}' not found")

    associations = disease_data["associatedTargets"]["rows"]
    
    # Sort by score (descending) to ensure highest scoring targets come first
    sorted_associations = sorted(associations, key=lambda x: x.get("score", 0), reverse=True)
    
    if return_ensembl_ids:
        return [
            row["target"].get("id", "")
            for row in sorted_associations
        ]
    else:
        return [
            row["target"].get("approvedSymbol", "")
            for row in sorted_associations
        ]


def get_target_drugs(
    target_ids: List[str],
    limit: int = 10
) -> Dict[str, List[str]]:
    """
    Query Open Targets GraphQL API for approved drugs associated with targets.

    Args:
        target_ids: List of target identifiers (e.g., Ensembl IDs like 'ENSG00000157764')
        limit: Maximum number of drugs to return per target

    Returns:
        Dictionary where keys are target IDs and values are lists of approved drug names
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    # GraphQL query to get known drugs for a specific target
    query = """
    query TargetDrugs($targetId: String!, $limit: Int!) {
      target(ensemblId: $targetId) {
        id
        approvedSymbol
        approvedName
        knownDrugs(
          size: $limit
        ) {
          count
          rows {
            drug {
              id
              name
            }
            phase
            status
          }
        }
      }
    }
    """

    result_dict = {}

    for target_id in target_ids:
        variables = {
            "targetId": target_id,
            "limit": limit
        }

        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"Warning: GraphQL errors for target {target_id}: {data['errors']}")
            result_dict[target_id] = []
            continue

        target_data = data["data"]["target"]
        if target_data is None:
            print(f"Warning: Target with ID '{target_id}' not found")
            result_dict[target_id] = []
            continue

        # Extract drug names from the response
        known_drugs = target_data.get("knownDrugs", {})
        if known_drugs is None:
            result_dict[target_id] = []
            continue

        drug_rows = known_drugs.get("rows", [])
        drug_names = [
            row["drug"].get("name", "")
            for row in drug_rows
            if row.get("drug") and row["drug"].get("name")
        ]

        # Remove duplicates by converting to set and back to list
        result_dict[target_id] = list(set(drug_names))

    return result_dict


def search_disease_by_name(
    disease_name: str
) -> str:
    """
    Search for a disease by name using the Open Targets GraphQL API.
    Returns the disease ID (EFO/MONDO ID) of the best match.

    Args:
        disease_name: Disease name to search for (e.g., 'asthma', 'diabetes')

    Returns:
        Disease ID of the best match (e.g., 'MONDO_0004979', 'EFO_0000270')
        Returns None if no disease is found.
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    query = """
    query searchDiseases($queryString: String!, $entityNames: [String!]) {
      search(queryString: $queryString, entityNames: $entityNames, page: {size: 1, index: 0}) {
        total
        hits {
          id
          name
          entity
          description
        }
      }
    }
    """

    variables = {
        "queryString": disease_name,
        "entityNames": ["disease"]
    }

    try:
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")

        search_results = data["data"]["search"]
        if search_results is None or not search_results.get("hits"):
            raise Exception(f"No disease found for name '{disease_name}'")

        # Return only the ID of the first (best) match
        return search_results["hits"][0]["id"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed for disease name '{disease_name}': {e}")


def search_drugs_by_name(
    drug_names: List[str],
    limit: int = 5
) -> Dict[str, List[Dict]]:
    """
    Search for drugs by name using the Open Targets GraphQL API.

    Args:
        drug_names: List of drug names to search for (e.g., 'aspirin', 'imatinib')
        limit: Maximum number of search results to return per drug name

    Returns:
        Dictionary where keys are search terms (drug names) and values are lists of matching drugs.
        Each drug dictionary contains:
        - id: ChEMBL ID
        - name: Drug name
        - entity: Type (should be 'drug')
        - description: Brief description
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    query = """
    query searchDrugs($queryString: String!, $entityNames: [String!], $size: Int!) {
      search(queryString: $queryString, entityNames: $entityNames, page: {size: $size, index: 0}) {
        total
        hits {
          id
          name
          entity
          description
        }
      }
    }
    """

    # Get unique drug names
    unique_drug_names = list(set(drug_names))
    result_dict = {}

    for drug_name in unique_drug_names:
        variables = {
            "queryString": drug_name,
            "entityNames": ["drug"],
            "size": limit
        }

        try:
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"Warning: GraphQL errors for drug name '{drug_name}': {data['errors']}")
                result_dict[drug_name] = []
                continue

            search_results = data["data"]["search"]
            if search_results is None:
                result_dict[drug_name] = []
                continue

            # Store the list of matching drugs
            result_dict[drug_name] = search_results.get("hits", [])

        except requests.exceptions.RequestException as e:
            print(f"Warning: Request failed for drug name '{drug_name}': {e}")
            result_dict[drug_name] = []
            continue

    return result_dict


def get_drugs_info(
    drug_ids: List[str],
    search_by_name: bool = True
) -> Dict[str, Dict]:
    """
    Query Open Targets GraphQL API for detailed information about drugs.

    Args:
        drug_ids: List of drug identifiers. If search_by_name=False, these should be 
                 ChEMBL IDs (e.g., 'CHEMBL1201589'). If search_by_name=True, these 
                 should be drug names (e.g., 'aspirin', 'imatinib').
                 Duplicates will be automatically removed.
        search_by_name: If True, treat drug_ids as drug names and search for them first.
                       If False (default), treat drug_ids as ChEMBL IDs.

    Returns:
        Dictionary where keys are drug ChEMBL IDs (or drug names if search failed) 
        and values are dictionaries containing:
        - id: ChEMBL ID
        - name: Drug name
        - description: Drug description
        - maximumClinicalTrialPhase: Highest clinical trial phase reached (1-4)
        - mechanismsOfAction: Dictionary with 'rows' containing list of mechanism dictionaries
          - Each mechanism has: mechanismOfAction, targetName, actionType, targets
          - targets is a list with: id, approvedSymbol, approvedName
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    query = """
    query DrugInfo($chemblId: String!) {
      drug(chemblId: $chemblId) {
        id
        name
        description
        maximumClinicalTrialPhase
        mechanismsOfAction {
          rows {
            mechanismOfAction
            targetName
            actionType
            targets {
              id
              approvedSymbol
              approvedName
            }
          }
        }
      }
    }
    """

    # If searching by name, first get ChEMBL IDs
    if search_by_name:
        search_results = search_drugs_by_name(drug_ids, limit=1)
        # Map names to ChEMBL IDs (taking the first match)
        name_to_id = {}
        for name, hits in search_results.items():
            if hits:
                name_to_id[name] = hits[0]['id']
            else:
                print(f"Warning: No drugs found for name '{name}'")
        unique_drug_ids = list(name_to_id.values())
    else:
        # Get unique drug IDs
        unique_drug_ids = list(set(drug_ids))
    
    result_dict = {}

    for drug_id in unique_drug_ids:
        variables = {
            "chemblId": drug_id
        }

        try:
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"Warning: GraphQL errors for drug {drug_id}: {data['errors']}")
                result_dict[drug_id] = None
                continue

            drug_data = data["data"]["drug"]
            if drug_data is None:
                print(f"Warning: Drug with ChEMBL ID '{drug_id}' not found")
                result_dict[drug_id] = None
                continue

            # Store the drug information
            result_dict[drug_id] = drug_data

        except requests.exceptions.RequestException as e:
            print(f"Warning: Request failed for drug {drug_id}: {e}")
            result_dict[drug_id] = None
            continue

    return result_dict