# 🐦 Nido de Cuco

> *A lightweight Linux decoy-file monitoring system for defensive security.*

**Nido de Cuco** es una herramienta defensiva ligera para sistemas Linux que despliega y monitorea archivos señuelo (*canarios digitales*). Su objetivo es actuar como un sensor de detección temprana, notificando cuando un usuario o proceso interactúa con un archivo que normalmente no debería ser tocado.

---

## 🎯 Filosofía y Concepto

En la administración de sistemas y la seguridad defensiva, contar con acceso o credenciales válidas no garantiza que todas las acciones realizadas dentro del sistema sean normales. Un empleado puede actuar por curiosidad, un script puede cometer un error o una cuenta legítima puede haber sido comprometida.

**Nido de Cuco** aborda este problema colocando trampas silenciosas en lugares estratégicos:
* `.env.produccion`
* `backup_finanzas.zip`
* `id_rsa_BACKUP`

Si alguien intenta leer, abrir o copiar uno de estos señuelos, el sistema captura el evento y recopila información relevante para su análisis.

> ⚠️ **Nota de precisión técnica:** Una interacción con un señuelo es una señal para la investigación, no una prueba automática de intrusión maliciosa. El objetivo es proporcionar contexto útil (*quién, qué, cuándo*) para determinar la naturaleza del evento.

---

## 🛠️ Funcionamiento Técnico

El sistema utiliza mecanismos de monitoreo del sistema de archivos en Linux (`inotify`) para observar los archivos señuelo con un consumo de recursos prácticamente nulo.

Al detectarse una interacción, **Nido de Cuco** captura:
1. **Archivo afectado:** El señuelo específico interactuado.
2. **Evento:** Tipo de acceso (`OPEN`, `READ`, etc.).
3. **Usuario:** Identidad que ejecutó la acción.
4. **Proceso y PID:** Nombre del programa (`cat`, `cp`, `python3`) y su identificador.
5. **Proceso Padre:** Contexto de ejecución (ej. `bash`).
6. **Timestamp:** Marca de tiempo precisa del evento.

---

## 🚀 Uso Rápido

### 1. Clonar el repositorio
```bash
git clone [https://github.com/eduar-q/nido-de-cuco.git](https://github.com/eduar-q/nido-de-cuco.git)
cd nido-de-cuco

```

### 2. Ejecutar el monitoreo

```bash
python3 nido_cuco.py --watch

```

---

## 📊 Ejemplo de Alerta

Cuando ocurre una interacción con un señuelo, la herramienta genera una salida en consola estructurada:

```text
╔══════════════════════════════════════════════════╗
║        ⚠️ DECOY INTERACTION — REVIEW REQUIRED     ║
╚══════════════════════════════════════════════════╝

📁 File:      .env.produccion
⚡ Event:     OPEN / ACCESS
👤 User:      eduar
⚙️ Process:   cat
🔢 PID:       4217
🌳 Parent:    bash
🕒 Time:      2026-10-21T15:24:10

[!] Notice: An interaction with a decoy is a signal 
    for investigation, not proof of malicious activity.

```

Además, los registros se almacenan en formato JSON (`events.json`) para facilitar su integración con herramientas de análisis de logs.

---

## 🔍 Limitaciones Explícitas

Para mantener la honestidad técnica del proyecto:

* **Dependencia de inotify:** Observa eventos a nivel de sistema de archivos; no realiza inspección profunda a nivel de kernel mediante eBPF o auditd.
* **Atacantes experimentados:** Un adversario con conocimiento avanzado del entorno podría evitar interactuar con archivos con nombres evidentemente tentadores.
* **Falsos positivos:** Herramientas automáticas de respaldo, indexadores de búsqueda o antivirus locales pueden activar eventos al escanear el directorio.

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT.
