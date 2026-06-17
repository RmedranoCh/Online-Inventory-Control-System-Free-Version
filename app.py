import io
from flask import Flask, jsonify, request, send_file, render_template
from src.utils.excel_exporter import generar_reporte_excel

app = Flask(__name__)

MAX_PRODUCTOS = 10
MAX_EXCEL = 2
MAX_STR_LEN = 500
MAX_HISTORIAL = 500


@app.after_request
def agregar_headers_seguridad(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), interest-cohort=()"
    )
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/excel", methods=["POST"])
def exportar_excel():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    productos = data.get("productos", [])
    historial = data.get("historial", [])
    excel_count = data.get("excel_count", 0)

    if not isinstance(excel_count, int):
        excel_count = int(excel_count) if str(excel_count).isdigit() else 0

    if not isinstance(productos, list) or not isinstance(historial, list):
        return jsonify({"error": "Formato inválido"}), 400

    if not productos:
        return jsonify({"error": "No hay productos para exportar"}), 400

    if len(productos) > MAX_PRODUCTOS:
        return jsonify({"error": "Demasiados productos"}), 400

    if len(historial) > MAX_HISTORIAL:
        historial = historial[:MAX_HISTORIAL]

    for p in productos:
        if not isinstance(p.get("nombre"), str) or len(p.get("nombre", "")) > MAX_STR_LEN:
            return jsonify({"error": "Nombre de producto inválido"}), 400
        for k in ("cantidad", "precio_costo", "stock_minimo"):
            v = p.get(k)
            if not isinstance(v, (int, float)):
                return jsonify({"error": f"Valor inválido en '{k}'"}), 400

    if excel_count >= MAX_EXCEL:
        return jsonify({
            "error": f"Límite alcanzado: máximo {MAX_EXCEL} archivos Excel en la versión gratuita"
        }), 403

    output = io.BytesIO()
    exito = generar_reporte_excel(output, productos, historial)

    if not exito:
        return jsonify({"error": "Error al generar el reporte"}), 500

    output.seek(0)
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="reporte_contable.xlsx",
    )


if __name__ == "__main__":
    import os
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
