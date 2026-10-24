"""Catalogo publico de NYC Systems.

Se publica cuando un ciudadano menciona al bot y escribe `comandos` despues de
la mencion. El texto es largo a proposito (es el manual de referencia del
servidor), asi que se reparte en varios embeds en vez de intentar colarlo en
uno solo: Discord limita cada descripcion a 4096 caracteres y cada mensaje a 10
embeds.
"""

import re
import discord
from bot.embeds import COLOR_INFO

EMBED_DESCRIPTION_LIMIT = 3800
EMBEDS_PER_MESSAGE = 10

CATALOG_FOOTER = "NYC Systems • Official Community Management System"
TRIGGER_WORD = r"comandos"

CATALOG_SECTIONS = [
    (
        "\U0001F1FA\U0001F1F8 NYC SYSTEMS",
        "**Sistema oficial de gestión de la comunidad**\n\n"
        "> \U0001F916 **¡Hola, comunidad!**\n"
        ">\n"
        "> Soy **NYC Systems**, el sistema encargado de gestionar y conectar gran parte "
        "de las funciones de nuestra comunidad.\n"
        ">\n"
        "> A través de mis comandos podrás administrar tu **identidad, personajes, "
        "economía, vehículos, propiedades, empleos, empresas, departamentos, armas, "
        "justicia, emergencias y mucho más**.\n"
        ">\n"
        "> Mi objetivo es hacer que la experiencia de rol sea más organizada, realista y "
        "sencilla para todos.",
    ),
    (
        "\U0001FAAA IDENTIDAD Y PERSONAJES",
        "Puedes crear y administrar tus propios ciudadanos mediante el sistema de DNI.\n\n"
        "`/dni crear` — Crea un nuevo personaje utilizando tu avatar de Roblox.\n"
        "`/dni solicitar` — Acceso alternativo para crear tu DNI.\n"
        "`/dni mis_personajes` — Consulta y administra tus personajes.\n"
        "`/dni ver` — Consulta una ficha ciudadana.\n"
        "`/dni buscar` — Busca ciudadanos mediante su número de DNI.\n"
        "`/dni revocar` — Revocación o suspensión de DNI para personal autorizado.\n\n"
        "\U0001F464 **Puedes tener hasta 5 personajes por usuario.**",
    ),
    (
        "\U0001F3AE CONEXIÓN CON ROBLOX",
        "También puedo conectar tu cuenta de Discord con Roblox.\n\n"
        "`/roblox vincular`\n"
        "`/roblox perfil`\n"
        "`/roblox desvincular`\n\n"
        "Con `/roblox perfil` podrás consultar una tarjeta con el **avatar 3D y "
        "estadísticas** del usuario.",
    ),
    (
        "\U0001F4B5 ECONOMÍA",
        "La economía de NYC Systems permite administrar tu dinero de forma completamente "
        "integrada.\n\n"
        "`/balance` — Consulta tu efectivo y banco.\n"
        "`/sueldo` / `/salario` — Cobra tu salario.\n"
        "`/pagar` — Envía dinero a otro ciudadano.\n"
        "`/donar` — Realiza donaciones.\n"
        "`/diario` — Recompensa diaria.\n"
        "`/semanal` — Recompensa semanal.\n"
        "`/tabla` — Rankings económicos, de nivel o reputación.\n"
        "`/nivel` — Consulta tu nivel.",
    ),
    (
        "\U0001F3E6 BANCO E INVERSIONES",
        "¿Quieres administrar tus finanzas?\n\n"
        "`/banco info`\n"
        "`/banco depositar`\n"
        "`/banco retirar`\n"
        "`/banco ahorros`\n"
        "`/banco prestamo`\n"
        "`/banco pagar`\n\n"
        "También puedes invertir mediante:\n\n"
        "`/invertir crear`\n"
        "`/invertir portafolio`\n\n"
        "\U0001F4B0 **Los ahorros generan un 2% diario.**",
    ),
    (
        "\U0001F6D2 TIENDAS Y MERCADOS",
        "Puedes comprar, vender e intercambiar diferentes objetos.\n\n"
        "**\U0001F3EA Tienda**\n"
        "`/tienda explorar`\n"
        "`/tienda comprar`\n"
        "`/tienda info`\n\n"
        "**\U0001F576️ Mercado negro**\n"
        "`/mercadonegro explorar`\n"
        "`/mercadonegro comprar`\n\n"
        "**\U0001F6CD️ Mercado ciudadano**\n"
        "`/mercado lista`\n"
        "`/mercado vender`\n"
        "`/mercado comprar`\n"
        "`/mercado pujar`\n"
        "`/mercado cancelar`\n\n"
        "También puedes administrar tus objetos mediante:\n\n"
        "`/inventario`",
    ),
    (
        "\U0001F52B ARMAS",
        "NYC Systems mantiene un registro individual de las armas.\n\n"
        "`/arma registrar`\n"
        "`/arma mis_armas`\n"
        "`/arma ver`\n"
        "`/arma transferir`\n"
        "`/arma incautar`\n\n"
        "\U0001F50E Cada arma registrada posee una **serie balística única**.",
    ),
    (
        "\U0001F697 VEHÍCULOS",
        "Registra y administra tus vehículos directamente desde Discord.\n\n"
        "`/vehiculo registrar`\n"
        "`/vehiculo mis_vehiculos`\n"
        "`/vehiculo ver`\n"
        "`/vehiculo buscar`\n"
        "`/vehiculo transferir`\n"
        "`/vehiculo reportar`\n"
        "`/vehiculo liberar`\n"
        "`/vehiculo incautar`\n\n"
        "\U0001F698 El sistema admite vehículos convencionales, **trailers y ATVs**, "
        "incluyendo placas personalizadas.",
    ),
    (
        "\U0001F3DB️ DEPARTAMENTOS Y FLOTAS",
        "Los departamentos pueden administrar sus miembros, presupuesto y vehículos "
        "oficiales.\n\n"
        "`/departamento lista`\n"
        "`/departamento info`\n"
        "`/departamento presupuesto`\n"
        "`/departamento miembros`\n"
        "`/departamento unirse`\n"
        "`/departamento mis_postulaciones`\n\n"
        "**\U0001F693 Flota**\n"
        "`/flota ver`\n"
        "`/flota catalogo`\n"
        "`/flota solicitar`\n"
        "`/flota devolver`\n"
        "`/flota reparar`\n\n"
        "Los mandos autorizados también cuentan con herramientas para **gestionar personal, "
        "vehículos y recursos departamentales**.",
    ),
    (
        "\U0001F4BC EMPLEOS PÚBLICOS",
        "Consulta y administra tus empleos:\n\n"
        "`/empleos listar`\n"
        "`/empleos mios`\n"
        "`/empleos entrar`\n"
        "`/empleos renunciar`\n\n"
        "Los administradores disponen de herramientas adicionales para crear y administrar "
        "empleos.",
    ),
    (
        "\U0001F3E2 EMPRESAS",
        "¿Quieres tener tu propio negocio?\n\n"
        "Con NYC Systems puedes crear una empresa y administrar prácticamente todos sus "
        "aspectos:\n\n"
        "**Empresa**\n"
        "`/empresa crear`\n"
        "`/empresa mi_empresa`\n"
        "`/empresa panel`\n"
        "`/empresa info`\n"
        "`/empresa disolver`\n\n"
        "**Finanzas**\n"
        "`/empresa caja`\n"
        "`/empresa nomina`\n"
        "`/empresa dinero`\n\n"
        "**Personal**\n"
        "`/empresa plantilla`\n\n"
        "**Productos y servicios**\n"
        "`/empresa menu`\n"
        "`/empresa catalogo`\n\n"
        "**Acciones**\n"
        "`/empresa sociedad`\n\n"
        "**Negocio**\n"
        "`/empresa negocio`\n\n"
        "\U0001F4C8 podrás contratar empleados, administrar nóminas, manejar las "
        "finanzas, vender productos, ofrecer servicios e incluso gestionar acciones de tu "
        "empresa.",
    ),
    (
        "\U0001F3E0 PROPIEDADES",
        "También puedo ayudarte a administrar tus propiedades.\n\n"
        "`/propiedad lista`\n"
        "`/propiedad comprar`\n"
        "`/propiedad rentar`\n"
        "`/propiedad mias`\n"
        "`/propiedad vender`\n\n"
        "\U0001F3E1 Al vender una propiedad recibirás el **75% de su valor**.",
    ),
    (
        "\U0001F46E POLICÍA Y JUSTICIA",
        "Las autoridades cuentan con herramientas especiales para administrar el sistema "
        "policial y judicial.\n\n"
        "`/policia arrestar`\n"
        "`/policia multar`\n"
        "`/policia antecedentes`\n"
        "`/policia mis_multas`\n"
        "`/policia pagar_multa`\n"
        "`/policia pagar_fianza`\n\n"
        "\U0001F510 **Estos comandos están restringidos al personal autorizado.**",
    ),
    (
        "\U0001F6A8 B.O.L.O. Y EXPEDIENTES",
        "La investigación policial también forma parte de NYC Systems.\n\n"
        "**\U0001F50E B.O.L.O.**\n"
        "`/bolo emitir`\n"
        "`/bolo lista`\n"
        "`/bolo ver`\n"
        "`/bolo actualizar`\n"
        "`/bolo borrar`\n\n"
        "**\U0001F4C1 Expedientes**\n"
        "`/caso abrir`\n"
        "`/caso lista`\n"
        "`/caso ver`\n"
        "`/caso nota_agregar`\n"
        "`/caso sospechoso_vincular`\n"
        "`/caso evidencia_vincular`\n"
        "`/caso estado`\n\n"
        "\U0001F510 Las funciones de gestión de expedientes están reservadas para "
        "**STAFF, JUECES y DETECTIVES autorizados**.",
    ),
    (
        "\U0001F4DE CENTRAL 911",
        "¿Existe una emergencia?\n\n"
        "El sistema 911 permite crear y gestionar incidentes:\n\n"
        "`/incidente crear`\n"
        "`/incidente lista`\n"
        "`/incidente ver`\n"
        "`/incidente atender`\n"
        "`/incidente cerrar`\n\n"
        "\U0001F694\U0001F691 **Policía y EMS pueden responder a los incidentes "
        "correspondientes.**",
    ),
    (
        "\U0001F575️ ACTIVIDADES CRIMINALES",
        "Dentro del sistema de rol también existen actividades criminales:\n\n"
        "`/drogas sembrar`\n"
        "`/drogas cosechar`\n"
        "`/drogas info`\n"
        "`/lavar dinero`\n"
        "`/lavar info`\n"
        "`/misiones`\n\n"
        "⚠️ **Estas funciones representan exclusivamente actividades dentro del "
        "sistema de rol.**",
    ),
    (
        "\U0001F4BC TRABAJOS SECUNDARIOS",
        "También puedes realizar trabajos adicionales:\n\n"
        "`/trabajar`\n"
        "`/trabajo mis_trabajos`\n\n"
        "El personal autorizado puede gestionar las evidencias mediante:\n\n"
        "`/trabajo pendientes`\n"
        "`/trabajo aprobar`\n"
        "`/trabajo rechazar`",
    ),
    (
        "⭐ REPUTACIÓN",
        "Tu comportamiento dentro de la comunidad también puede reflejarse en tu "
        "reputación.\n\n"
        "`/reputacion perfil`\n"
        "`/reputacion dar`",
    ),
    (
        "\U0001F3AB TICKETS Y VERIFICACIÓN",
        "**\U0001F3AB Tickets**\n"
        "`/ticket abrir`\n"
        "`/ticket cerrar`\n\n"
        "El personal administrativo dispone además del panel y configuración del "
        "sistema.\n\n"
        "**✅ Verificación**\n"
        "`/verificar estado`\n"
        "`/verificar panel`\n"
        "`/verificar configurar`\n"
        "`/verificar agregar_rol`\n"
        "`/verificar remover_rol`\n"
        "`/verificar ver_config`\n"
        "`/verificar revocar`",
    ),
    (
        "\U0001F4D6 ¿NO SABES QUÉ COMANDO UTILIZAR?",
        "No te preocupes.\n\n"
        "Puedes utilizar:\n\n"
        "**`/help`**\n\n"
        "o\n\n"
        "**`/ayuda`**\n\n"
        "\U0001F4DA Encontrarás un **manual interactivo organizado por categorías**, "
        "donde podrás consultar los comandos disponibles y aprender cómo utilizar cada "
        "sistema.",
    ),
    (
        "\U0001F1FA\U0001F1F8 NYC SYSTEMS",
        "> **Un solo sistema. Toda una comunidad.**\n"
        ">\n"
        "> \U0001FAAA Identidad\n"
        "> \U0001F4B5 Economía\n"
        "> \U0001F3E6 Banca\n"
        "> \U0001F697 Vehículos\n"
        "> \U0001F3E0 Propiedades\n"
        "> \U0001F46E Policía\n"
        "> \U0001F691 Emergencias\n"
        "> \U0001F3E2 Empresas\n"
        "> \U0001F3DB️ Departamentos\n"
        "> ⚖️ Justicia\n"
        "> ⭐ Reputación\n"
        "> \U0001F3AB Comunidad\n"
        ">\n"
        "> **Todo administrado desde un mismo lugar.**\n"
        ">\n"
        "> — **NYC Systems**\n"
        "> *Official Community Management System*",
    ),
]


def mention_pattern(bot_user_id: int) -> re.Pattern:
    """Encuentra la mencion al bot admitiendo `<@id>` y `<@!id>` (el nick legacy)."""
    return re.compile(rf"<@!?{bot_user_id}>")


def wants_catalog(content: str, bot_user_id: int) -> bool:
    """True si el mensaje menciona al bot y despues de la mencion dice `comandos`.

    Exige el orden menciona -> "comandos": un "comandos" suelto antes del ping no
    cuenta, para no responder a cualquier frase que Mention la palabra.
    """
    mention = mention_pattern(bot_user_id).search(content)
    if not mention:
        return False
    after = content[mention.end():]
    return re.search(rf"\b{TRIGGER_WORD}\b", after, re.IGNORECASE) is not None


def _group_sections() -> list[list[tuple[str, str]]]:
    """Agrupa bloques mientras quepan en la descripcion de un embed."""
    groups: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    budget = 0

    for title, body in CATALOG_SECTIONS:
        # +8 del separador y del encabezado en negrita de los bloques siguientes.
        cost = len(title) + len(body) + 8
        if current and budget + cost > EMBED_DESCRIPTION_LIMIT:
            groups.append(current)
            current = []
            budget = 0
        current.append((title, body))
        budget += cost

    if current:
        groups.append(current)
    return groups


def build_catalog_embeds() -> list[discord.Embed]:
    """Un embed por grupo de secciones, respetando los limites de Discord."""
    groups = _group_sections()
    total = len(groups)
    embeds = []
    for index, group in enumerate(groups, 1):
        title, body = group[0]
        description = body
        for extra_title, extra_body in group[1:]:
            description += f"\n\n**{extra_title}**\n{extra_body}"

        # El contenido no cabe en un solo embed, asi que se numera para que se
        # lea como una serie y no como dos mensajes sin relacion.
        if total > 1:
            title = f"{title}  ({index}/{total})"

        embed = discord.Embed(
            title=title,
            description=description[:EMBED_DESCRIPTION_LIMIT],
            color=COLOR_INFO,
        )
        embed.set_footer(text=CATALOG_FOOTER)
        embeds.append(embed)
    return embeds


def build_catalog_messages() -> list[list[discord.Embed]]:
    """Los embeds partidos en los mensajes queDiscord permitira enviar."""
    embeds = build_catalog_embeds()
    return [embeds[i:i + EMBEDS_PER_MESSAGE]
            for i in range(0, len(embeds), EMBEDS_PER_MESSAGE)]
