import random


async def change_title(api):
    titles_list = [
        "SCB", "СЦБ", "SCBeu", "СЦБеу", "<𝑺𝑪𝑩>", "<𝕾𝕮𝕭>", "<🅂🄲🄱>", "＼（＾○＾） <𝑺𝑪𝑩> （＾○＾）／",
        "ツ 𝑺𝑪𝑩 ツ", "( ͡• ͜ʖ ͡• ) <𝑺𝑪𝑩> ( ͡• ͜ʖ ͡• )", "(^ᴥ^) <𝑺𝑪𝑩> (^ᴥ^)", "───==≡≡ΣΣ(づ￣ ³￣)づ 𝑺𝑪𝑩",
        "𝑺𝑪𝑩  ━╤デ╦︻(▀̿̿Ĺ̯̿̿▀̿ ̿)", "СЭЦЭБЭ", "СЦБебра", "СЦБЕК"
    ]
    title = random.choice(titles_list)
    await api.api.groups.edit(group_id=api.group_id, title=title)
    print("Title changed!")