# ADN RFID ERP

## Descripción general
ADN RFID ERP es una aplicación desarrollada sobre el marco **Frappe/ERPNext** para automatizar la generación y gestión de etiquetas RFID asociadas a artículos, activos y números de serie dentro de los flujos de inventario. El proyecto introduce lógica de servidor, personalizaciones de DocTypes y extensiones de interfaz que permiten:

* Generar identificadores únicos para artículos, activos y series durante la creación o actualización de documentos.
* Encolar etiquetas en un DocType específico (`RFID Print Queue`) a partir de transacciones de inventario o acciones masivas en listas.
* Exponer utilidades HTTP para crear transacciones de inventario desde integraciones externas.

El repositorio contiene el paquete instalable `rfid`, compatible con las herramientas `bench` de Frappe, junto con fixtures y recursos necesarios para desplegar la aplicación en un sitio ERPNext.

## Arquitectura de la solución
La aplicación sigue la arquitectura estándar de Frappe, separando lógica de negocio por DocType y reutilizando el sistema de eventos y hooks de la plataforma:

1. **Eventos de DocType**: se utilizan ganchos declarados en `hooks.py` para interceptar acciones en `Item`, `Stock Entry` y `Asset`, generando códigos RFID o encolando etiquetas según el momento del ciclo de vida del documento.【F:rfid/hooks.py†L31-L58】
2. **DocTypes personalizados**: se define el DocType `RFID Print Queue` con campos específicos para rastrear la generación e impresión de etiquetas.【F:rfid/rfid/doctype/rfid_print_queue/rfid_print_queue.json†L1-L74】
3. **API Whitelist**: funciones expuestas mediante `@frappe.whitelist()` permiten integrar procesos externos (por ejemplo, creación de transacciones de inventario o carga masiva de etiquetas).【F:rfid/rfid/api.py†L12-L89】【F:rfid/rfid/api.py†L94-L109】
4. **Personalizaciones de interfaz**: scripts de lista en JavaScript amplían las vistas de `Serial No` y `Asset`, añadiendo acciones de un clic para enviar registros a la cola de impresión RFID.【F:rfid/rfid/doctype/serial_no/serial_no_list.js†L1-L19】【F:rfid/rfid/doctype/asset/asset_list.js†L1-L13】
5. **Fixtures y configuraciones**: los archivos de fixtures aplican campos adicionales y reordenamientos de formulario para soportar los nuevos flujos RFID dentro de ERPNext.【F:rfid/fixtures/custom_field.json†L1-L46】【F:rfid/fixtures/property_setter.json†L1-L22】

Esta arquitectura garantiza que la funcionalidad se integre de manera nativa con los procesos estándar de ERPNext sin modificar el núcleo de la plataforma.

## Estructura del proyecto
| Ruta | Descripción |
| --- | --- |
| `rfid/` | Paquete principal del app Frappe, con metadatos, hooks y recursos estáticos. |
| `rfid/config/` | Configuración de escritorio y documentación del módulo, incluida la definición del módulo "Rfid" en el escritorio de ERPNext.【F:rfid/config/desktop.py†L1-L10】 |
| `rfid/fixtures/` | Exportaciones de fixtures para campos personalizados (`custom_rfid`) y ajustes de formularios.【F:rfid/fixtures/custom_field.json†L1-L46】【F:rfid/fixtures/property_setter.json†L1-L22】 |
| `rfid/rfid/api.py` | Lógica de servidor expuesta para generación de etiquetas, colas de impresión y creación de transacciones.【F:rfid/rfid/api.py†L12-L109】 |
| `rfid/rfid/doctype/` | Implementaciones específicas por DocType (Python, JSON, JS) que amplían los procesos estándar de ERPNext.【F:rfid/rfid/doctype/rfid_print_queue/rfid_print_queue.json†L1-L74】 |
| `rfid/public/` | Carpeta reservada para activos estáticos; incluye `.gitkeep` para mantener la estructura del paquete.【F:rfid/public/.gitkeep†L1-L1】 |
| `rfid/www/` y `rfid/templates/` | Puntos de extensión para páginas web personalizadas (actualmente sin contenido específico). |
| `modules.txt`, `patches.txt` | Declaración del módulo y espacio para parches de migración utilizados por `bench`. |

## Componentes principales

### Hooks de servidor
El archivo `hooks.py` registra los eventos clave del sistema:

* **`Item.before_save`**: asigna códigos de barras RFID únicos a los artículos y asegura que tengan series de números de serie predefinidas.【F:rfid/hooks.py†L38-L45】【F:rfid/rfid/doctype/item/item.py†L1-L12】
* **`Stock Entry.on_submit`**: tras registrar una entrada de almacén, genera RFID individuales para cada número de serie creado y los persiste en el DocType estándar `Serial No`.【F:rfid/hooks.py†L45-L47】【F:rfid/rfid/doctype/stock_entry/stock_entry.py†L1-L18】
* **`Asset.before_save`**: sincroniza los activos con sus artículos asociados y agrega un RFID exclusivo si el artículo tiene uno configurado.【F:rfid/hooks.py†L47-L49】【F:rfid/rfid/doctype/asset/asset.py†L1-L8】

### DocType `RFID Print Queue`
El DocType personalizado actúa como búfer de etiquetas pendientes de impresión, registrando el código del artículo, estado, cantidad y el valor RFID generado.【F:rfid/rfid/doctype/rfid_print_queue/rfid_print_queue.json†L1-L74】 Su clase Python hereda directamente de `Document`, ya que la lógica principal reside en las funciones API que crean los registros.【F:rfid/rfid/doctype/rfid_print_queue/rfid_print_queue.py†L1-L9】

### API y utilidades
El módulo `rfid.rfid.api` concentra la lógica transaccional:

* **`create_print_rfid_se`**: al recibir un `Stock Entry`, recupera los números de serie generados y crea entradas en la cola de impresión, mostrando mensajes de confirmación en la interfaz.【F:rfid/rfid/api.py†L12-L58】
* **`create_print_rfid_sn`**: procesa acciones masivas desde las listas de `Serial No` o `Asset` para encolar etiquetas a demanda.【F:rfid/rfid/api.py†L60-L89】
* **`generate_unique_hex`**: usa `secrets.token_hex` para generar códigos de longitud variable, garantizando unicidad criptográficamente segura.【F:rfid/rfid/api.py†L91-L92】
* **`create_se`**: servicio HTTP que permite a sistemas externos crear entradas de almacén (material receipt) con ítems, cantidades y precios proporcionados en el cuerpo de la solicitud.【F:rfid/rfid/api.py†L94-L109】

### Extensiones de interfaz (JavaScript)
Los scripts de lista agregan acciones personalizadas en la UI de ERPNext:

* **Lista de `Serial No`**: incorpora la acción "Print RFID" que llama al método `create_print_rfid_sn` con los registros seleccionados.【F:rfid/rfid/doctype/serial_no/serial_no_list.js†L1-L19】
* **Lista de `Asset`**: reutiliza el mismo flujo para activos, reutilizando el método API y adaptando el origen de datos para obtener el código RFID del campo `custom_rfid`.【F:rfid/rfid/doctype/asset/asset_list.js†L1-L13】

### Personalizaciones y fixtures
Los fixtures permiten reproducir la configuración en múltiples sitios:

* **Campo `custom_rfid` en `Asset`**: añade un campo tipo código de barras, de sólo lectura, para almacenar la etiqueta generada.【F:rfid/fixtures/custom_field.json†L1-L46】
* **Reordenamiento del formulario de `Asset`**: asegura que el campo `custom_barcode` y secciones relacionadas aparezcan en posiciones coherentes al momento de desplegar la aplicación.【F:rfid/fixtures/property_setter.json†L1-L22】

## Flujo funcional del RFID
1. **Creación/actualización de artículo**: al guardar un `Item`, se genera un `custom_barcode` y se prepara la serie de números de serie para futuras transacciones.【F:rfid/rfid/doctype/item/item.py†L1-L12】
2. **Recepción de inventario**: al enviar una `Stock Entry`, cada número de serie relacionado recibe un RFID único almacenado en su campo `custom_barcode`.【F:rfid/rfid/doctype/stock_entry/stock_entry.py†L1-L18】
3. **Gestión de activos**: cuando se guarda un `Asset`, se asocia un `custom_rfid` basado en el artículo vinculado, manteniendo sincronizados los identificadores en ambos lados.【F:rfid/rfid/doctype/asset/asset.py†L1-L8】
4. **Encolado para impresión**: desde cualquier número de serie, activo o la propia transacción de inventario, se pueden crear entradas en `RFID Print Queue`, quedando listas para ser procesadas por el sistema de impresión o integraciones posteriores.【F:rfid/rfid/api.py†L12-L89】

## Dependencias y stack tecnológico
* **Frappe/ERPNext**: el proyecto se instala como aplicación adicional dentro de un sitio Frappe gestionado con `bench`. La dependencia principal se gestiona desde el ecosistema Frappe y se instala mediante `bench init` según la convención documentada en `requirements.txt`.【F:requirements.txt†L1-L1】
* **Lenguajes**: la lógica de servidor utiliza Python (DocTypes y APIs), la capa de interfaz emplea JavaScript para personalizar vistas de lista, y los metadatos de DocType/fixtures se describen en JSON. También se incluyen archivos de configuración en texto plano (`modules.txt`, `patches.txt`).
* **Bibliotecas estándar**: se aprovechan módulos nativos como `secrets` para la generación criptográfica de IDs, además de utilidades provistas por Frappe como `frappe.db`, `frappe.new_doc` y `frappe.utils` para operaciones sobre documentos y UI.【F:rfid/rfid/api.py†L1-L109】

## Puesta en marcha y desarrollo
1. **Preparar entorno Frappe**: instalar Frappe/ERPNext con `bench init` y crear un sitio mediante `bench new-site`.
2. **Agregar la aplicación**:
   ```bash
   bench get-app path/to/adn-rfid-erp
   bench --site <tu-sitio> install-app rfid
   ```
3. **Aplicar fixtures**: ejecutar `bench --site <tu-sitio> migrate` para que los fixtures y personalizaciones se sincronicen con la base de datos.
4. **Desarrollo**:
   * Modificar la lógica de servidor en `rfid/rfid/doctype/*/*.py` o `rfid/rfid/api.py`.
   * Actualizar scripts de interfaz en `rfid/rfid/doctype/*/*.js`.
   * Exportar cambios de personalización mediante `bench --site <tu-sitio> export-fixtures`.
5. **Pruebas**: las clases de prueba heredan de `FrappeTestCase`, permitiendo crear suites automatizadas para validar las integraciones con ERPNext.【F:rfid/rfid/doctype/rfid_print_queue/test_rfid_print_queue.py†L1-L10】

## Mantenimiento y contribución
* **Convenciones**: seguir la estructura modular de Frappe, agrupando lógica por DocType y evitando modificar archivos del núcleo de ERPNext.
* **Extensiones futuras**: se pueden añadir acciones adicionales en `hooks.py` para otros DocTypes, o extender el DocType `RFID Print Queue` con workflows y estados personalizados.
* **Documentación**: actualizar este README y los docstrings en los módulos Python cuando se introduzcan nuevos procesos o dependencias.

Con esta documentación, cualquier desarrollador familiarizado con Frappe puede instalar, comprender y extender el módulo RFID para adaptarlo a necesidades específicas de gestión de activos e inventario.
