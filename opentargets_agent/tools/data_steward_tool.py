def get_target_data_from_opentargets(target: str) -> dict:
    """Retrieves data related to a specified target.

    Args:
        target (str): The name of the target for which to retrieve data.

    Returns:
        dict: status and result or error msg.
    """
    if target.lower() == "braf":
        return {
            "status": "success",
            "report": (
                "The BRAF gene is located on chromosome 7 and is involved in cell signaling."
            )
        }
    else:
        return {
            "status": "error",
            "error_message": f"Data for target '{target}' is not available.",
        }