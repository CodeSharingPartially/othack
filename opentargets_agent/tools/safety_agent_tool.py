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
    Retrieve target prioritization scores from various sources for a list of targets using the Open Targets GraphQL API.

    This function queries prioritization scores for each target and returns a dictionary mapping each Ensembl ID to its prioritization data.

    Args:
        ensembl_ids (List[str]): List of Ensembl gene IDs.

    Returns:
        Dict[str, Any]: Dictionary where keys are Ensembl IDs and values are prioritization information or error details.

    Prioritization information includes:
        - items: List of key-value pairs representing prioritization metrics from different sources
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
