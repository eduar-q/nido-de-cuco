# 🐦 Nido de Cuco

> *A lightweight Linux decoy-file monitoring system for defensive security.*

**Nido de Cuco** es una herramienta defensiva ligera para sistemas Linux que utiliza archivos señuelo (*decoy files*) como pequeños sensores de actividad.

La idea es sencilla: colocar archivos que no contienen información sensible real y que, en condiciones normales, no deberían necesitar ser utilizados. Si se detecta actividad sobre ellos, **Nido de Cuco** genera una señal para facilitar su posterior investigación.

---

## 🎯 Filosofía y Concepto

Tener credenciales válidas o acceso autorizado a un sistema no significa que todas las acciones realizadas dentro de él sean necesariamente esperadas.

Un usuario puede acceder a un archivo por curiosidad, una herramienta automática puede inspeccionarlo, una cuenta legítima puede haber sido comprometida o una persona con acceso autorizado puede realizar una acción fuera de lo habitual.

**Nido de Cuco** explora este problema utilizando archivos señuelo con nombres como:

- `.env.produccion`
- `backup_finanzas.zip`
- `id_rsa_BACKUP`

Estos archivos **no contienen credenciales, claves privadas ni información sensible real**.

Cuando el sistema detecta actividad sobre uno de los señuelos, registra el evento para que pueda ser revisado posteriormente.

> ⚠️ **Una interacción con un señuelo es una señal para investigar, no una prueba automática de actividad maliciosa.**

El objetivo de la herramienta no es decidir quién es un atacante, sino detectar interacciones que merecen una segunda mirada.

---

## 🛠️ Funcionamiento Técnico

**Nido de Cuco** utiliza `inotify`, el mecanismo de notificación de eventos del sistema de archivos disponible en Linux, para observar específicamente los archivos señuelo.

Dependiendo del tipo de interacción, pueden observarse eventos como:

- `OPEN` — apertura del archivo.
- `ACCESS` — acceso al contenido.
- `MODIFY` — modificación.
- `ATTRIB` — cambio de atributos.
- `CLOSE` — cierre del archivo.
- `DELETE` — eliminación.
- `MOVE` — movimiento o cambio de ubicación.

La herramienta registra información como:

1. **Archivo:** señuelo sobre el que ocurrió el evento.
2. **Evento:** operación observada por `inotify`.
3. **Timestamp:** momento en el que se detectó la actividad.
4. **Contexto adicional:** información que la implementación pueda obtener de forma verificable durante el análisis del evento.

> ⚠️ `inotify` informa de eventos del sistema de archivos, pero no proporciona por sí solo una atribución completa y fiable del usuario o proceso responsable de cada evento.

---

## 📁 Estructura del Proyecto

```text
nido-de-cuco/
├── decoys/
│   ├── .env.produccion
│   ├── backup_finanzas.zip
│   └── id_rsa_BACKUP
│
├── examples/
│   ├── alert.example.txt
│   └── events.example.json
│
├── events.json
├── nido_cuco.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### `decoys/`

Contiene los archivos señuelo utilizados por el sistema.

Los archivos son ficticios y no deben contener información sensible real.

### `examples/`

Contiene ejemplos de las alertas y eventos generados por la herramienta.

### `events.json`

Archivo generado durante la ejecución para almacenar los eventos detectados.

Este archivo se considera **salida local de ejecución** y no debe contenerse en el repositorio público.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/eduar-q/nido-de-cuco.git
cd nido-de-cuco
```

### 2. Crear un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

La herramienta utiliza:

```text
inotify_simple==1.3.5
```

---

## ▶️ Uso

Para iniciar el monitoreo:

```bash
python3 nido_cuco.py --watch
```

La herramienta comenzará a observar los archivos señuelo configurados.

> Ejecuta la herramienta únicamente en sistemas propios o donde tengas autorización para realizar este tipo de monitoreo.

---

## 📊 Ejemplo de Alerta

Cuando se detecta actividad sobre un señuelo, la herramienta genera una salida estructurada similar a esta:

```text
╔══════════════════════════════════════════════════╗
║       ⚠ DECOY INTERACTION — REVIEW REQUIRED     ║
╚══════════════════════════════════════════════════╝

📁 File:      .env.produccion
⚡ Event:     OPEN
🕒 Time:      2026-10-21T15:24:10

[!] Notice:
An interaction with a decoy is a signal for
investigation, not proof of malicious activity.
```

Los eventos también pueden almacenarse en formato JSON para facilitar su revisión, conservación o procesamiento posterior.

Ejemplo:

```json
[
    {
        "timestamp": "2026-10-21 15:24:10",
        "file": ".env.produccion",
        "event": "OPEN",
        "user": "example-user"
    }
]
```

---

## 🔍 Interpretación de una Alerta

Una alerta de **Nido de Cuco** no significa automáticamente:

> “Hay un atacante dentro del sistema.”

Puede existir una explicación legítima.

Por ejemplo:

- Un usuario abrió el archivo accidentalmente.
- Un administrador estaba inspeccionando el directorio.
- Un indexador examinó el archivo.
- Una herramienta de respaldo accedió a él.
- Un antivirus realizó un análisis.
- Una cuenta legítima está siendo utilizada de manera inesperada.

Por eso, la clasificación utilizada es:

```text
REVIEW REQUIRED
```

La herramienta detecta la interacción.

**La investigación humana determina su significado.**

---

## 🧠 ¿Por qué utilizar archivos señuelo?

Un archivo señuelo funciona como un pequeño sensor.

No necesita contener información real para resultar útil. Su valor está precisamente en que **normalmente nadie debería necesitar interactuar con él**.

Por eso, una interacción puede convertirse en un punto de partida para investigar qué ocurrió y determinar si corresponde a una actividad legítima, accidental, automatizada o potencialmente sospechosa.

El concepto también contempla un escenario importante:

```text
Cuenta legítima
      ↓
Acceso autorizado
      ↓
Interacción inesperada
      ↓
Señuelo
      ↓
REVIEW REQUIRED
```

La autenticación demuestra que una cuenta pudo acceder al sistema.

No demuestra por sí sola que todo lo que esa cuenta haga después sea esperado.

---

## 🔍 Limitaciones

El proyecto mantiene deliberadamente un alcance pequeño y sus resultados deben interpretarse teniendo en cuenta las siguientes limitaciones:

- **`inotify` observa eventos del sistema de archivos:** no proporciona por sí solo una atribución completa y fiable del usuario, PID o proceso responsable de cada evento.
- **No realiza inspección profunda:** esta versión no utiliza mecanismos como `auditd`, `fanotify` o eBPF para realizar atribución avanzada de actividad.
- **Un atacante puede reconocer los señuelos:** un adversario experimentado podría identificar determinados nombres como posibles archivos trampa y decidir no interactuar con ellos.
- **Pueden existir eventos legítimos:** indexadores, herramientas de respaldo, antivirus y otros procesos automáticos pueden acceder a los señuelos.
- **Una alerta no demuestra compromiso:** los eventos requieren contexto e investigación antes de obtener conclusiones.

Estas limitaciones son parte del diseño del proyecto:

> **Nido de Cuco funciona como un sensor defensivo, no como un sistema completo de detección de intrusiones.**

---

## 🔐 Seguridad

Los archivos señuelo utilizados por el proyecto deben contener exclusivamente información falsa.

Nunca deben utilizarse:

- Contraseñas reales.
- Tokens reales.
- Claves SSH reales.
- Credenciales de servicios.
- Información privada.
- Datos pertenecientes a clientes o terceros.

El objetivo es detectar interacción sin introducir nuevos secretos o información sensible en el sistema.

---

## 🧪 Ejemplo de Escenario

Un administrador coloca un archivo señuelo:

```text
.env.produccion
```

El archivo no contiene credenciales reales.

Horas después, se detecta una interacción:

```text
File: .env.produccion
Event: OPEN
Time: 2026-10-21 15:24:10
```

La herramienta no concluye que existe un atacante.

El administrador puede entonces revisar:

- Qué estaba ocurriendo en ese momento.
- Qué procesos estaban activos.
- Qué usuario estaba trabajando.
- Si existía una tarea automatizada.
- Si la actividad era esperada.
- Si existen otros indicadores que justifiquen una investigación.

El señuelo funciona como **punto de observación**, no como veredicto.

---

## 🧩 Idea Central

**Nido de Cuco no intenta adivinar quién es un atacante.**

Detecta interacción con algo que normalmente no debería necesitar ser tocado y genera una señal para investigar.

```text
Decoy file
    │
    ▼
Interaction
    │
    ▼
Filesystem event
    │
    ▼
Nido de Cuco
    │
    ▼
REVIEW REQUIRED
    │
    ▼
Human investigation
```

---

## ⚖️ Autorización

Esta herramienta está diseñada para fines defensivos y debe utilizarse únicamente en sistemas propios o en sistemas donde exista autorización explícita para realizar monitoreo.

No contiene mecanismos de explotación ni pretende reemplazar una investigación de seguridad completa.

---

## 📜 Licencia

Este proyecto está distribuido bajo la **Licencia MIT**.

---

## 👨‍💻 Author

**Eduar Q.**

*Linux · Python · Defensive Security · System Administration*
