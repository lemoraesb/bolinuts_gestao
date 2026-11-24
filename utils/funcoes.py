from datetime import datetime, date
import pandas as pd


def numero(valor, padrao=0.0):
    """Converte valores numéricos legados sem interromper a aplicação."""
    try:
        if valor in (None, ""):
            return float(padrao)
        return float(valor)
    except (TypeError, ValueError):
        return float(padrao)


def buscar_pedidos(colecao):
    return list(colecao.find().sort("_id", -1))


def gerar_codigo_pedido(colecao):
    maior_numero = 0
    for pedido in colecao.find({}, {"codigo_pedido": 1}):
        codigo = pedido.get("codigo_pedido", "")
        try:
            numero_codigo = int(str(codigo).replace("BOL-", ""))
            maior_numero = max(maior_numero, numero_codigo)
        except (ValueError, TypeError):
            continue
    return f"BOL-{maior_numero + 1:03d}"


def resumo_financeiro(pedido):
    """Calcula total, recebido, saldo e status sem confiar em campos derivados antigos.

    Para registros antigos marcados como pagos, mas sem valor de sinal informado,
    considera o total como recebido. Não altera o documento no MongoDB.
    """
    total = numero(pedido.get("valor_total"))
    recebido = numero(pedido.get("valor_sinal"))
    status_original = str(pedido.get("status_pagamento", "")).strip().lower()

    if status_original == "pago" and recebido <= 0 and total > 0:
        recebido = total

    recebido = min(max(recebido, 0.0), max(total, 0.0))
    restante = max(total - recebido, 0.0)

    if total > 0 and restante <= 0.009:
        status = "Pago"
    elif recebido > 0:
        status = "Parcial"
    else:
        status = "Pendente"

    return {
        "total": round(total, 2),
        "recebido": round(recebido, 2),
        "restante": round(restante, 2),
        "status": status,
    }


def calcular_status(valor_total, valor_sinal):
    total = max(numero(valor_total), 0.0)
    recebido = min(max(numero(valor_sinal), 0.0), total)
    if total > 0 and recebido >= total:
        return "Pago"
    if recebido > 0:
        return "Parcial"
    return "Pendente"


def formatar_valor(valor):
    return f"R$ {numero(valor):.2f}".replace(".", ",")


def converter_data(valor):
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        try:
            return pd.to_datetime(valor, dayfirst=True).date()
        except Exception:
            pass
    return None


def obter_massas(pedido):
    massas = pedido.get("massas", pedido.get("massa", []))
    if isinstance(massas, str):
        return [massas] if massas else []
    return massas or []


def obter_decoracao(pedido):
    decoracao = pedido.get("decoracao", "")
    if isinstance(decoracao, list):
        return ", ".join(str(item) for item in decoracao)
    return str(decoracao or "")
