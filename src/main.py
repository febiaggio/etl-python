import argparse

from functions import (
    hash_field,
    int_to_float,
    item_to_dict,
    json_to_dicts_list,
    timestap_to_datetime,
    to_tsv,
)

if __name__ == "__main__":
    # CLI options
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Absolute or relative path for the input file.")
    parser.add_argument(
        "--hash",
        action="store_true",
        help="If you want to hash sensitive fields.",
    )
    args = parser.parse_args()

    # TSV options
    headers_tsv = [
        "venda_id",
        "venda_dt",
        "cliente_email",
        "distribuidora_id",
        "entrega_tipo",
        "produto_id",
        "produto_valor",
        "item_id",
        "item_qtd",
    ]

    # Execution
    dictionary_list = json_to_dicts_list(args.input)
    orders = int_to_float(dictionary_list)
    orders = timestap_to_datetime(orders)
    if args.hash:
        hash_field(orders)
    orders = item_to_dict(orders)
    to_tsv(orders, headers_tsv)
