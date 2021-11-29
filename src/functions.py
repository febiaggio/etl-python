import csv
import hashlib
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Union

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def json_to_dicts_list(filepath: str) -> Dict[str, Union[str, int]]:
    """Load JSON file into a dictionary
    Args:
        filepath (str): Valid filesystem path for the input file.
    Returns:
        Dict[str, Union[str, int]]: Dictionary containing the loaded data.
    """
    with open(filepath, "r") as file:
        try:
            dictionary_list = json.load(file)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            logger.error(
                "Invalid input file. Check if the file contains valid JSON text."
            )
            sys.exit()
    return dictionary_list


def hash_field(dictionary_list: list) -> Dict[str, Union[str, int]]:
    """Hash sensitive fields
    Args:
        dictionary_list (list): Dictionary list.
    Returns:
        Dict[str, Union[str, int]]: Dictionary list containing hash fields.
    """
    for order in dictionary_list:
        try:
            hash_field = ""
            hash_field = hashlib.sha256()
            hash_field.update(order["cliente_email"].encode("utf-8"))
            order["cliente_email"] = hash_field.hexdigest()
        except KeyError as e:
            logger.error(e)
            logger.error(
                "Invalid input. Check if the dictionary list contains a specified key"
            )
            sys.exit()
    return dictionary_list


def int_to_float(dictionary_list: list) -> Dict[str, Union[str, int]]:
    """Convert column "produto_valor" to float
    Args:
        dictionary_list (list): Dictionary list.
    Returns:
        Dict[str, Union[str, int]]: Dictionary list.
    """
    for order in dictionary_list:
        for produto in order["produtos"]:
            try:
                float_value = float(produto["valor"] / 100)
                produto["valor"] = f"{float_value:.2f}"
            except KeyError as e:
                logger.error(e)
                logger.error(
                    "Invalid input. Check if the dictionary list contains a specified key"
                )
                sys.exit()
    return dictionary_list


def timestap_to_datetime(dictionary_list: list) -> Dict[str, Union[str, int]]:
    """Convert column "produto_valor" to float
    Args:
        dictionary_list (list): Dictionary list.
    Returns:
        Dict[str, Union[str, int]]: Dictionary list.
    """
    for order in dictionary_list:
        try:
            order["venda_dt"] = (datetime.fromtimestamp(order["venda_dt"])).isoformat()
        except KeyError as e:
            logger.error(e)
            logger.error(
                "Invalid input. Check if the dictionary list contains a specified key"
            )
            sys.exit()
    return dictionary_list


def item_to_dict(dictionary_list: dict) -> Dict[str, Union[str, int]]:
    """Create a new dictionary list using items as index
    Args:
        dictionary_list (list): Dictionary list.
    Returns:
        Dict[str, Union[str, int]]: Dictionary list using items as index.
    """
    list_by_items = []
    for orders in dictionary_list:
        for products in orders["produtos"]:
            for items in products["itens"]:
                try:
                    lista = [
                        orders["venda_id"],
                        orders["venda_dt"],
                        orders["cliente_email"],
                        orders["distribuidora_id"],
                        orders["entrega_tipo"],
                        products["id"],
                        products["valor"],
                        items,
                        products["quantidade"]
                    ]
                    list_by_items.append(lista)
                except TypeError as e:
                    logger.error(e)
                    logger.error(
                        "Invalid input. Check if the input contains a dictionary list"
                    )
                    sys.exit()
    return list_by_items


def to_tsv(dictionary_list: list, headers: list) -> None:
    """Convert dictionary list to tsv
    Args:
        dictionary_list (list): Dictionary list.
    """
    with open(
        os.path.normpath(os.getcwd() + os.sep + os.pardir)
        + "/outputs/vendas_"
        + str(datetime.utcnow().strftime("%Y%m%d_%H%M%S%f"))
        + ".tsv",
        "wt",
        encoding="utf-8",
        newline="",
    ) as file:
        try:
            tsv_writer = csv.writer(file, delimiter="\t")
            tsv_writer.writerow(headers)
            for line in dictionary_list:
                tsv_writer.writerow(line)
        except FileNotFoundError as e:
            logger.error(e)
            logger.error("Invalid directory. Check if the directory really exists")
            sys.exit()
    return print("Successfully generated .tsv file in /outputs directory")
