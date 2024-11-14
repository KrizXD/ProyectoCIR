Informe Técnico del Proyecto de Plataforma Administrativa para Organización de Empleados
1. Introducción
Este proyecto consistió en el desarrollo de una plataforma administrativa para la organización y gestión de empleados en mesones de trabajo, empleando Django como framework backend, SQLite como base de datos y tecnologías de frontend como HTML, CSS y JavaScript. El sistema fue diseñado para ser inclusivo y accesible, especialmente enfocado en simplificar las interfaces para que sean comprensibles y fáciles de usar por empleados con discapacidades cognitivas.
2. Objetivos del Proyecto
•	Facilitar la asignación de empleados a mesones de trabajo mediante una interfaz administrativa intuitiva.
•	Proporcionar una experiencia inclusiva en la interfaz de usuario para empleados con distintas discapacidades cognitivas.
•	Optimizar el acceso a la información de trabajo para empleados y jefes de mesón.
3. Funcionalidades del Sistema
El sistema contempla tres tipos de vistas de usuario, cada una con diferentes permisos y funcionalidades:
1.	Vista de Empleados:
o	Muestra la asignación de mesones y el jefe de mesa correspondiente.
o	Incluye fotografías de los empleados para facilitar la identificación.
o	La interfaz está simplificada para garantizar que sea accesible y fácil de entender para empleados con discapacidades cognitivas.
2.	Vista de Administradores:
o	Permite a los administradores asignar y mover empleados entre los mesones.
o	La interfaz permite organizar visualmente a los empleados en cada área de trabajo.
3.	Vista de Superadministradores:
o	Incluye todas las funcionalidades anteriores.
o	Agrega capacidades avanzadas, como crear, editar o eliminar empleados y supervisar las acciones de los administradores.
o	Permite la administración de configuraciones adicionales y monitoreo de actividad.
4. Desafíos Técnicos
•	Inclusividad y accesibilidad: La interfaz para empleados fue diseñada para ser lo más clara y simple posible, utilizando un lenguaje visual intuitivo y minimizando el texto en beneficio de iconos e imágenes que faciliten su comprensión.
•	Gestión de permisos: La plataforma implementa un sistema de roles de usuario que permite restringir el acceso y la capacidad de modificación de acuerdo con el tipo de usuario logeado.
•	Integración visual de datos: El diseño se enfocó en una disposición visual de los mesones y empleados, haciendo uso de CSS para lograr una estructura limpia y organizada.
5. Tecnología Utilizada
•	Django y SQLite: Django se utilizó como backend, proporcionando el sistema de gestión de usuarios, mientras que SQLite funcionó como la base de datos para almacenar la información de los empleados y los registros de actividad.
•	HTML, CSS y JavaScript: Se utilizaron para construir una interfaz amigable e interactiva. CSS ayudó a dar estructura visual y consistencia, mientras que JavaScript se usó para añadir interactividad en la asignación de empleados y visualización de los mesones.
6. Conclusión
El proyecto alcanzó su objetivo de crear una plataforma inclusiva y funcional para la organización de empleados en mesones de trabajo, respondiendo a las necesidades de accesibilidad para personas con discapacidades cognitivas. Los desafíos se enfocaron en la creación de una interfaz simplificada, la gestión de permisos y el despliegue visual de datos, los cuales fueron exitosamente abordados. Esta plataforma ofrece una herramienta eficiente para administrar la asignación de empleados y mantener el orden en los espacios de trabajo de manera inclusiva y accesible.

