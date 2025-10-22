import requests
from typing import List, Dict, Any

def get_target_tractability(ensembl_ids: List[str]) -> Dict[str, Any]:
    """
    Retrieve tractability assessment for a list of targets from the Open Targets GraphQL API.

    This function queries the tractability of each target, including antibody and small molecule tractability, and returns a dictionary mapping each Ensembl ID to its tractability data.

    Args:
        ensembl_ids (List[str]): List of Ensembl gene IDs (e.g., ['ENSG00000141510']).

    Returns:
        Dict[str, Any]: Dictionary where keys are Ensembl IDs and values are tractability information or error details.

    The tractability information includes:
        - modality: Type of tractability (e.g., antibody, small molecule)
        - value: Assessment value
        - label: Human-readable label
    """
    graphql_query = """
    query TargetTractability($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            tractability {
                modality
                value
                label
            }
        }
    }
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"
    results = {}
    for ensembl_id in ensembl_ids:
        variables = {"ensemblId": ensembl_id}
        response = requests.post(
            url,
            json={"query": graphql_query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            results[ensembl_id] = {"error": data["errors"]}
        else:
            results[ensembl_id] = data.get("data", {}).get("target", {})
    return results

def get_target_chemical_probes(ensembl_ids: List[str]) -> Dict[str, Any]:
    """
    Retrieve chemical probes for target validation for a list of targets using the Open Targets GraphQL API.

    This function queries chemical probes, including quality scores and probe metadata, for each target and returns a dictionary mapping each Ensembl ID to its chemical probe data.

    Args:
        ensembl_ids (List[str]): List of Ensembl gene IDs.

    Returns:
        Dict[str, Any]: Dictionary where keys are Ensembl IDs and values are chemical probe information or error details.

    Chemical probe information includes:
        - id: Probe identifier
        - control: Control status
        - drugId: Associated drug ID
        - isHighQuality: Boolean indicating probe quality
        - mechanismOfAction: Mechanism of action
        - origin: Source of probe
        - probesDrugsScore, probeMinerScore, scoreInCells, scoreInOrganisms: Various quality scores
        - targetFromSourceId: Source target ID
        - urls: List of related URLs
    """
    graphql_query = """
    query TargetChemicalProbes($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            chemicalProbes {
                id
                control
                drugId
                isHighQuality
                mechanismOfAction
                origin
                probesDrugsScore
                probeMinerScore
                scoreInCells
                scoreInOrganisms
                targetFromSourceId
                urls { niceName, url }
            }
        }
    }
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"
    results = {}
    for ensembl_id in ensembl_ids:
        variables = {"ensemblId": ensembl_id}
        response = requests.post(
            url,
            json={"query": graphql_query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            results[ensembl_id] = {"error": data["errors"]}
        else:
            results[ensembl_id] = data.get("data", {}).get("target", {})
    return results

def get_target_prioritization(ensembl_ids: List[str]) -> Dict[str, Any]:
    """
    Retrieve comprehensive target prioritization scores for evaluating potential drug targets using the Open Targets GraphQL API.

    Target prioritization is a scoring system that helps researchers assess the viability and promise of potential drug targets
    across four main dimensions:

    1. Precedence: Clinical history and validation
       - Measures maximum clinical trial phase reached for the target
       - Source: ChEMBL database
       - Higher scores indicate targets with clinical precedent

    2. Tractability: Druggability assessment
       - Evaluates protein characteristics such as membrane location, secretion status, ligand binding,
         small molecule interactions, and predicted binding pockets
       - Indicates how amenable the target is to drug development

    3. Doability: Research feasibility
       - Assesses practical aspects like mouse ortholog identity, availability of chemical probes,
         and comparative genomics
       - Measures how easily the target can be studied experimentally

    4. Safety: Risk assessment
       - Analyzes potential liabilities through genetic constraint metrics (gnomAD), mouse phenotypes,
         gene essentiality (DepMap), known safety events, cancer driver status, and tissue specificity
       - Identifies potential adverse effects or toxicity concerns

    Interpreting Scores:
    The prioritization system uses a "traffic light" scoring approach where:
    - Green (positive values) indicates potentially favorable attributes
    - Red (negative values) suggests potentially unfavorable attributes or concerns

    Score Ranges and Interpretation:
    - Precedence (0 to 1): Based on maximum clinical trial phase; higher = more clinical validation
    - Tractability (0, 1, or NA):
      * 1 = Positive druggability features present (membrane protein, binding pockets, etc.)
      * 0 = Feature absent or neutral
      * NA = No data available
    - Genetic Constraint (-1 to 1):
      * -1 = Least tolerant to loss-of-function (essential gene, higher safety concern)
      * 1 = Most tolerant to loss-of-function (lower safety concern)
      * 0 = Neutral constraint
    - Safety Events (-1 or 0):
      * -1 = Known adverse events, cancer driver genes, or significant safety concerns
      * 0 = No known safety concerns
    - Tissue Specificity (-1 to 1):
      * Higher values = More tissue-specific expression (potentially safer, fewer off-target effects)
      * -1 = Low specificity (expressed broadly, higher risk of off-target effects)

    Args:
        ensembl_ids (List[str]): List of Ensembl gene IDs.

    Returns:
        Dict[str, Any]: Dictionary where keys are Ensembl IDs and values are prioritization information or error details.

    Prioritization information includes:
        - items: List of key-value pairs where keys are metric names (e.g., 'clinical_precedence',
                'predicted_tractability', 'mouse_ortholog') and values are the corresponding scores or assessments
    """
    graphql_query = """
    query TargetPrioritisation($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            prioritisation {
                items {
                    key
                    value
                }
            }
        }
    }
    """
    url = "https://api.platform.opentargets.org/api/v4/graphql"
    results = {}
    for ensembl_id in ensembl_ids:
        variables = {"ensemblId": ensembl_id}
        response = requests.post(
            url,
            json={"query": graphql_query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            results[ensembl_id] = {"error": data["errors"]}
        else:
            results[ensembl_id] = data.get("data", {}).get("target", {})
    return results


def get_target_safety_information(ensembl_ids: List[str]) -> Dict[str, Any]:
    """
    Retrieve safety liabilities and related information for a list of targets from the Open Targets GraphQL API.

    This function queries safety liabilities, biosamples, effects, studies, and literature for each target and returns a dictionary mapping each Ensembl ID to its safety information.

    Args:
        ensembl_ids (List[str]): List of Ensembl gene IDs.

    Returns:
        Dict[str, Any]: Dictionary where keys are Ensembl IDs and values are safety information or error details.

    Safety information includes:
        - safetyLiabilities: List of safety events and effects
        - biosamples: Details about cell and tissue samples
        - effects: Dosing and direction of effects
        - studies: Study metadata (name, type, description)
        - datasource: Source of safety data
        - literature: Related literature references
        - url: Link to further information
    """
    graphql_query = """
        query Safety($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            id
            safetyLiabilities {
            event
            eventId
            biosamples {
                cellFormat
                cellLabel
                tissueLabel
                tissueId
            }
            effects {
                dosing
                direction
            }
            studies {
                name
                type
                description
            }
            datasource
            literature
            url
            }
        }
        }
    """
    results = {}
    for ensembl_id in ensembl_ids:
            url = "https://api.platform.opentargets.org/api/v4/graphql"
            variables = {"ensemblId": ensembl_id}
            response = requests.post(
                url,
                json={"query": graphql_query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                results[ensembl_id] = {"error": data["errors"]}
            else:
                results[ensembl_id] = data.get("data", {}).get("target", {})
    return results
