
"""
“Commons Clause” License Condition v1.0
The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.
Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.
For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.
Software: XBot
License: Apache 2.0"""
import fortnitepy
import json
import os

import functools
import random
import time
import threading
import asyncio
import datetime as dt
from datetime import datetime
import crayons
import aiohttp


def console_success(bot_info, content):
    print(crayons.blue(bot_info) + crayons.green(f" {content}"))
def console_error(bot_info, content):
    print(crayons.blue(bot_info) + crayons.red(f" {content}"))
def now():
    return datetime.now().strftime("%H:%M:%S")
loop = asyncio.get_event_loop()
version = "1.9"
try:
    with open("config.json") as f:
        data = json.load(f)
except:
    with open("config.json", "w") as f:
        json.dump({'accounts': [{'email': 'email@email.com', 'password': 'your_password'}], 'friendaccept': True, 'defaultskin': 'renegade raider', 'defaultlevel': 123,
                   'defaultbackpack': 'black shield', 'defaultpickaxe': "raider's revenge", 'admin': '', 'platform': 'WIN'}, f, indent=4, sort_keys=False)
    print("Please fill out config.json before continuing. Closing this window in 5 seconds.")
    time.sleep(5)
    exit()
accounts = data["accounts"]
filename = 'device_auths.json'


async def fetch_id(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as a:
            if await a.json() == {'error': 'Could not find any cosmetic matching parameters'}:
                return None
            else:
                return (await a.json())["id"]

class default_cosmetics:
    def __init__(self):
        if "cid" in data["defaultskin"].lower():
            self.default_skin = data["defaultskin"]
        else:
            self.default_skin = loop.run_until_complete(fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={data['defaultskin']}&backendType=AthenaCharacter"))
        if "pickaxe" in data["defaultpickaxe"].lower():
            self.default_pickaxe = data["defaultpickaxe"]
        else:
            self.default_pickaxe = loop.run_until_complete(fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=full&name={data['defaultpickaxe']}&backendType=AthenaPickaxe"))
        if "bid" in data["defaultbackpack"].lower():
            self.defaultbackpack = data["defaultbackpack"]
        else:
            self.defaultbackpack = loop.run_until_complete(fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={data['defaultbackpack']}&backendType=AthenaBackpack"))

class bot_commands:
    def __init__(self):
        self.commands = {}

    def add_command(self, name=None):
        if name == None:
            def new_command(func):
                self.commands.update({f"!{func.__name__}": func})
            return new_command
        else:
            def custom_name(func):
                self.commands.update({f"!{name}": func})
            return custom_name

fortnite_commands = bot_commands()


class MyClient(fortnitepy.Client):
    def __init__(self, email, password):
        device_auth_details = self.get_device_auth_details().get(email, {})
        super().__init__(
            auth=fortnitepy.AdvancedAuth(
                email=email,
                password=password,
                prompt_authorization_code=True,
                delete_existing_device_auths=True,
                **device_auth_details
            ),
            platform=fortnitepy.Platform(data["platform"])
        )
        
    def get_device_auth_details(self):
        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)
        return {}

    def store_device_auth_details(self, email, details):
        existing = self.get_device_auth_details()
        existing[email] = details

        with open(filename, 'w') as fp:
            json.dump(existing, fp)

    async def event_device_auth_generate(self, details, email):
        self.store_device_auth_details(email, details)

    async def event_ready(self):
        print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(" Started!"))
        for a in list(self.pending_friends.values()):
            if a.incoming:
                await a.accept()

    async def event_friend_request(self, request):
        print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(f" Recieved friend request from {request.display_name}"))
        await request.accept()
        print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(f" Accepted friend request from {request.display_name}"))

    async def event_party_invite(self, invite):
        print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(f" Recieved party invite from {invite.sender.display_name}."))
        await invite.accept()
        print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(f" Joined {invite.sender.display_name}'s party."))
        await reset(self)

    async def event_party_member_join(self, member):
        if member.display_name != self.party.me.display_name:
            print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.green(f" {member.display_name} joined the party."))
        if self.party.member_count == 2:
            await reset(self)

    async def event_friend_message(self, message):
        print(crayons.blue(f"[{self.party.me.display_name}] [{message.author.display_name}] [{now()}] ") + crayons.green(message.content))
        command = message.content.split(" ", 1)
        #try:
        await fortnite_commands.commands[command[0]](message, command, self)
        """
        except KeyError as a:
            print(a)
            print(crayons.blue(f"[{self.party.me.display_name}] [{now()}]") + crayons.red(f" Unknown command '{message.content}'"))
        except Exception as a:
            print(a)
            print(crayons.blue(
                f"[X-Bot] [{now()}]: ") + crayons.red(f"Unknown command '{message.content}'"))"""
    async def event_party_member_leave(self, user):
        if self.party.member_count == 1 and user.display_name != self.party.me.display_name:
            await self.party.me.leave()

@fortnite_commands.add_command()
async def skin(message, msg, client):
    skin = await fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaCharacter")
    if skin == None:
        await message.reply("Please enter a valid skin name.")
    else:
        try:
            print(skin)
            await client.party.me.set_outfit(skin)
            await message.reply(f"Skin set to {skin}")
            console_success(f"[{client.party.me.display_name}] [{now()}]", f"Skin set to {skin}")
        except:
            console_error(f"[{client.party.me.display_name}] [{now()}]", f"An error occured.")
            await message.reply("An Unknown error occured.")

@fortnite_commands.add_command()
async def emote(message, msg, client):
    id = await fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaDance")
    if id == None:
        await message.reply("Please enter a valid emote.")
    else:
        try:
            await client.party.me.set_emote(id)
            await message.reply(f"Emote set to {id}")
        except:
            await message.reply("An Unknown error occured.")

@fortnite_commands.add_command()
async def backpack(message, msg, client):
    id = await fetch_id(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaBackpack")
    if id == None:
        await message.reply("Please enter a valid backpack.")
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_backpack(id)
            await message.reply(f"Backpack set to {id}")
        except:
            await message.reply("An unknown error occured.")

@fortnite_commands.add_command()
async def level(message, msg, client):
    try:
        await client.party.me.set_banner(season_level=int(msg[1]))
        await message.reply(f"Level set to {msg[1]}")
    except:
        await message.reply("Enter a valid number.")

@fortnite_commands.add_command()
async def henchman(message, msg, client):
    if msg[1].lower() == "ghost":
        await client.party.me.set_outfit("CID_707_Athena_Commando_M_HenchmanGood")
        await message.reply("Outfit set to ghost henchman.")
    elif msg[1].lower() == "shadow":
        await client.party.me.set_outfit("cid_npc_athena_commando_m_henchmanbad")
        await message.reply("Outfit set to shadow henchman.")

@fortnite_commands.add_command()
async def leave(message, msg, client):
    await client.party.me.leave()
    await message.reply("Left the party.")

@fortnite_commands.add_command()
async def battlepass(message, msg, client):
    try:
        await client.party.me.set_battlepass_info(has_purchased=True, level=int(msg[1]))
        await message.reply("Battlepass info updated.")
    except:
        await message.reply("Please enter a valid level.")

@fortnite_commands.add_command()
async def pinkghoul(message, msg, client):
    variants = client.party.me.create_variants(material=3)
    await client.party.me.set_outfit("CID_029_Athena_Commando_F_Halloween", variants=variants)
    await message.reply("Outfit set to the pink ghoul trooper.")

@fortnite_commands.add_command()
async def stop(message, msg, client):
    await client.party.me.clear_emote()
    await message.reply("Emote cleared.")

@fortnite_commands.add_command()
async def purpleskull(message, msg, client):
    variants = client.party.me.create_variants(clothing_color=1)
    await client.party.me.set_outfit("cid_030_athena_commando_m_halloween", variants=variants)
    await message.reply("Outfit set to the purple skull trooper.")

@fortnite_commands.add_command()
async def checkeredrenegade(message, msg, client):
    variants = client.party.me.create_variants(material=2)
    await client.party.me.set_outfit("CID_028_Athena_Commando_F", variants=variants)
    await message.reply("Outfit set to the checkered renegade raider.")

@fortnite_commands.add_command()
async def copy(message, msg, client):
    try:
        mem = client.party.members.get(
            message.author.id)  # get the sender's info
        await client.party.me.edit(
            functools.partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=mem.outfit,
                variants=mem.outfit_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_backpack,
                asset=mem.backpack,
                variants=mem.backpack_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=mem.pickaxe,
                variants=mem.pickaxe_variants
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=mem.banner[0],
                color=mem.banner[1],
                season_level=mem.banner[2]
            ),
            functools.partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=True,
                level=mem.battlepass_info[1]
            )
        )
        await message.reply("Copied their loadout!")
    except:
        await message.reply("Please enter a valid party member.")

@fortnite_commands.add_command()
async def ready(message, msg, client):
    await client.party.me.set_ready(fortnitepy.enums.ReadyState.READY)
    await message.reply("Ready")

@fortnite_commands.add_command()
async def unready(message, msg, client):
    await client.party.me.set_ready(fortnitepy.enums.ReadyState.NOT_READY)
    await message.reply("Unready")

@fortnite_commands.add_command()
async def sitout(message, msg, client):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await message.reply("Sitting Out")

@fortnite_commands.add_command()
async def rare(message, msg, client):
    await client.party.me.set_outfit("CID_028_Athena_Commando_F")
    await client.party.me.set_backpack("BID_004_BlackKnight")
    await client.party.me.set_pickaxe("Pickaxe_Lockjaw")
    await message.reply("Set to a rare loadout.")
@fortnite_commands.add_command(name="random")
async def random_a(message, msg, client):
    async with aiohttp.ClientSession() as request:
        async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaCharacter") as a:
            allcos = await a.json()
    length = len(allcos)
    cid = allcos[random.randint(1, length)]["id"]
    async with aiohttp.ClientSession() as request:
        async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaBackpack") as a:
            allcos = await a.json()
    length = len(allcos)
    bid = allcos[random.randint(1, length)]["id"]
    async with aiohttp.ClientSession() as request:
        async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaPickaxe") as a:
            allcos = await a.json()
    length = len(allcos)
    pid = allcos[random.randint(1, length)]["id"]
    await client.party.me.set_backpack(bid)
    await client.party.me.set_outfit(cid)
    await client.party.me.set_pickaxe(pid)
    await message.reply("Randomized the loadout.")

@fortnite_commands.add_command()
async def status(message, msg, client):
    await client.set_status(status=msg[1])
    await message.reply("Status set.")

@fortnite_commands.add_command()
async def loserfruit(message, msg, client):
    await client.party.me.set_outfit("CID_764_Athena_Commando_F_Loofah")
    await client.party.me.set_backpack("BID_527_Loofah")
    await client.party.me.set_emote("EID_Loofah")
    await message.reply("Set to loserfruit's loadout!")

@fortnite_commands.add_command()
async def goldenpeely(message, msg, client):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=4)
    await client.party.me.set_outfit("CID_701_Athena_Commando_M_BananaAgent", variants=variants, enlightenment=(2, 350))
    await message.reply("Outfit set to golden peely.")

@fortnite_commands.add_command()
async def mintyelf(message, msg, client):
    variants = fortnitepy.ClientPartyMember.create_variants(material=2)
    await client.party.me.set_outfit("CID_051_Athena_Commando_M_HolidayElf", variants=variants)
    await message.reply("Outfit set to minty elf.")

@fortnite_commands.add_command()
async def femalehenchman(message, msg, client):
    if msg[1].lower() == "ghost":
        await client.party.me.set_outfit("CID_NPC_Athena_Commando_F_HenchmanSpyGood")
        await message.reply("Outfit set to the female ghost henchman")
    elif msg[1].lower() == "shadow":
        await client.party.me.set_outfit("CID_NPC_Athena_Commando_F_HenchmanSpyDark")
        await message.reply("Outfit set to the female ghost henchman")

@fortnite_commands.add_command()
async def goldenskye(message, msg, client):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=4)
    await client.party.me.set_outfit("CID_690_Athena_Commando_F_Photographer", variants=variants, enlightenment=(2, 300))
    await message.reply("Skin set to golden skye")

@fortnite_commands.add_command()
async def point(message, msg, client):
    await client.party.me.set_emote("EID_IceKing")
    await message.reply("Pointing!")

@fortnite_commands.add_command()
async def vbucks(message, msg, client):
    await client.party.me.set_emote("EID_TakeTheL")
    await message.reply("Noob")

@fortnite_commands.add_command()
async def nobackpack(message, msg, client):
    await client.party.me.clear_backpack()
    await message.reply("Backpack cleared")

@fortnite_commands.add_command()
async def invite(message, msg, client):
    try:
        await message.author.invite()
        await message.reply("Invite sent")
    except fortnitepy.errors.HTTPException:
        await message.reply("Error code -91")


@fortnite_commands.add_command()
async def join(message, msg, client):
    await message.author.join_party()
    await asyncio.sleep(.5)
    await reset(client)
    await message.reply("Joined")

@fortnite_commands.add_command(name="reset")
async def reset_c(message, msg, client):
    await reset(client)
    await message.reply("Reset my loadout")

@fortnite_commands.add_command()
async def gift(message, msg, client):
    await client.party.me.set_emote("EID_MakeItRain")
    await asyncio.sleep(2)
    await client.party.me.set_emote("EID_TakeTheL")
    await asyncio.sleep(2)
    await client.party.me.clear_emote()
    await message.reply("Syke")

@fortnite_commands.add_command()
async def friend(message, msg, client):
    try:
        user = await client.fetch_profile_by_display_name(msg[1])
        await client.add_friend(user.id)
        await message.reply(f"Added user {user.id}")
    except:
        await message.reply(f"User {msg[1]} does not exist")

@fortnite_commands.add_command()
async def unfriend(message, msg, client):
    try:
        user = await client.fetch_profile_by_display_name(msg[1])
        await client.remove_or_decline_friend(user.id)
        await message.reply(f"Removed friend {user.id}")
    except:
        await message.reply(f"User {msg[1]} does not exist or is not friends")

@fortnite_commands.add_command()
async def promote(message, msg, client):
    user = await client.fetch_profile_by_display_name(msg[1])
    member = client.party.members.get(user.id)
    await member.promote()

@fortnite_commands.add_command()
async def vbuck_man(message, msg, client):
    await client.party.me.set_outfit("CID_129_Athena_Commando_M_Deco")
    await client.party.me.set_backpack("BID_069_DecoMale")
    await client.party.me.set_emote("EID_MakeItRain")
    await message.reply("Outfit set to vbuck man")

@fortnite_commands.add_command()
async def bp(message, msg, client):
    if msg[1] == "2":
        await client.party.me.set_outfit("CID_032_Athena_Commando_M_Medieval")
        await client.party.me.set_backpack("BID_002_RoyaleKnight")
        await client.party.me.set_pickaxe("Pickaxe_ID_012_District")
        await client.party.me.set_emote("Eid_IceKing")
        time.sleep(2)
        await client.party.me.set_outfit("CID_033_Athena_Commando_F_Medieval")
        await client.party.me.set_backpack("BID_002_RoyaleKnight")
        await client.party.me.set_emote("EID_Worm")
        time.sleep(2)
        await client.party.me.set_emote("EID_Floss")
        time.sleep(2)
        await client.party.me.set_outfit("CID_039_Athena_Commando_F_Disco")
        await client.party.me.set_pickaxe("Pickaxe_ID_013_Teslacoil")
        await client.party.me.set_emote("EID_IceKing")
        time.sleep(2)
        await client.party.me.set_outfit("CID_035_Athena_Commando_M_Medieval")
        await client.party.me.set_backpack("BID_004_BlackKnight")
        await message.reply("Done")
    elif msg[1].lower() == "3":
        await client.party.me.set_outfit("CID_080_Athena_Commando_M_Space")
        await client.party.me.set_pickaxe("Pickaxe_ID_027_Scavenger")
        await client.party.me.set_emote("Eid_IceKing")
        time.sleep(2)
        await client.party.me.set_outfit("CID_082_Athena_Commando_M_Scavenger")
        await client.party.me.set_emote("EID_TakeTheL")
        time.sleep(2)
        await client.party.me.set_backpack("BID_024_Space")
        await client.party.me.set_outfit("CID_081_Athena_Commando_F_Space")
        await client.party.me.set_emote("EID_BestMates")
        time.sleep(2)
        await client.party.me.set_outfit("CID_088_Athena_Commando_M_SpaceBlack")
        await client.party.me.set_backpack("BID_028_SpaceBlack")
        await client.party.me.set_outfit("CID_083_Athena_Commando_F_Tactical")
        await client.party.me.set_emote("EID_Robot")
        time.sleep(2)
        await client.party.me.set_outfit("CID_084_Athena_Commando_M_Assassin")
        await message.reply("Done")

@fortnite_commands.add_command()
async def hatlessrecon(message, msg, client):
    variants = fortnitepy.ClientPartyMember.create_variants(parts=2)
    await client.party.me.set_outfit("CID_022_Athena_Commando_F", variants=variants)

@fortnite_commands.add_command()
async def hologram(message, msg, client):
    await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")

@fortnite_commands.add_command()
async def pickaxe(message, msg, client):
    async with aiohttp.ClientSession() as request:
        async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaPickaxe") as a:
            response = await a.json()
    if response == []:
        await message.reply("Please enter a valid pickaxe name.")
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_pickaxe(id)
            await message.reply(f"Pickaxe set to {id}")
        except:
            await message.reply("An Unknown error occured.")

@fortnite_commands.add_command()
async def emoji(message, msg, client):
    async with aiohttp.ClientSession() as request:
        async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaEmoji") as a:
            response = await a.json()
    if response == []:
        await message.reply("Please enter a valid emoji name.")
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_emoji(id)
            await message.reply(f"Emoji set to {id}")

        except:
            await message.reply("An Unknown error occured.")

@fortnite_commands.add_command()
async def banner(message, msg, client):
    await client.party.me.set_banner(msg[1])
    await message.reply(f"Banner set to {msg[1]}")

@fortnite_commands.add_command()
async def playlist(message, msg, client):
    await client.party.set_playlist(playlist=msg[1], region=fortnitepy.Region.EUROPE)

@fortnite_commands.add_command()
async def maskedfade(message, msg, client):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=3)
    await client.party.me.set_outfit("CID_777_Athena_Commando_M_RacerZero", variants=variants)
    await message.reply("Skin set to masked fade")

@fortnite_commands.add_command()
async def variants(message, msg, client):
    try:
        content = msg[1].split(" ", 1)
        if content[0].isdigit():
            async with aiohttp.ClientSession() as request:
                async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=full&name={content[1]}") as a:
                    code = await a.json()
            type_v = code["variants"][0]["channel"].lower()
            variants = fortnitepy.ClientPartyMember.create_variants(
                **{type_v: content[0]}
            )
            if "cid" in code["id"].lower():
                await client.party.me.set_outfit(code["id"], variants=variants)
                await message.reply(f"Outfit set to {code['id']} with the {content[0]} variant.")
            elif "bid" in code["id"].lower():
                await client.party.me.set_backpack(code["id"], variants=variants)
                await message.reply(f"Backpack set to {code['id']} with the {content[0]} variant.")

            elif "pickaxe" in code["id"].lower():
                await client.party.me.set_pickaxe(code["id"], variants=variants)
                await message.reply(f"Pickaxe set to {code['id']} with the {content[0]} variant.")
        else:
            await message.reply("Please enter the command in a valid syntax.")
    except Exception as a:
        print(a)

@fortnite_commands.add_command()
async def style(message, msg, client):
    content = msg[1].split(" ", 2)
    if content[0].isdigit():
        async with aiohttp.ClientSession() as request:
            async with request.get(f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=full&name={content[2]}") as a:
                code = await a.json()
        type_v = content[1]
        variants = fortnitepy.ClientPartyMember.create_variants(
            **{type_v: content[0]}
        )
        if "cid" in code["id"].lower():
            await client.party.me.set_outfit(code["id"], variants=variants)
            await message.reply(f"Outfit set to {code['id']} with the {content[0]} variant.")
        elif "bid" in code["id"].lower():
            await client.party.me.set_backpack(code["id"], variants=variants)
            await message.reply(f"Backpack set to {code['id']} with the {content[0]} variant.")
        elif "pickaxe" in code["id"].lower():
            await client.party.me.set_pickaxe(code["id"], variants=variants)
            await message.reply(f"Pickaxe set to {code['id']} with the {content[0]} variant.")
    else:
        await message.reply("Please enter the command in a valid syntax.")

@fortnite_commands.add_command()
async def eternalknight(message, msg, client):
    variants = variants = fortnitepy.ClientPartyMember.create_variants(
        progressive=2, material=2)
    await client.party.me.set_outfit("CID_767_Athena_Commando_F_BlackKnight", variants=variants, enlightenment=(3, 160))
    await message.reply(f"Skin set to max eternal knight.")
@fortnite_commands.add_command()
async def cid(message, msg, client):
    await client.party.me.set_outfit(msg[1])
@fortnite_commands.add_command()
async def eid(message, msg, client):
    await client.party.me.set_emote(msg[1])
@fortnite_commands.add_command()
async def bid(message, msg, client):
    await client.party.me.set_backpack(msg[1])
@fortnite_commands.add_command()
async def threads(message, msg, time_c):
    await message.reply(f"Thread count: {threading.active_count()}")



default = default_cosmetics()
async def reset(client):
    await client.party.me.set_outfit(default.default_skin)
    await client.party.me.set_banner(season_level=123)
    await client.party.me.set_backpack(default.defaultbackpack)
    await client.party.me.set_pickaxe(default.default_pickaxe)

to_run = []
for x in accounts:
    to_run.append(MyClient(x["email"], x["password"]))

print(crayons.green("\n\n██╗  ██╗     ██████╗  ██████╗ ████████╗"))
print(crayons.green("╚██╗██╔╝     ██╔══██╗██╔═══██╗╚══██╔══╝"))
print(crayons.green(" ╚███╔╝█████╗██████╔╝██║   ██║   ██║   "))
print(crayons.green(" ██╔██╗╚════╝██╔══██╗██║   ██║   ██║   "))
print(crayons.green("██╔╝ ██╗     ██████╔╝╚██████╔╝   ██║   "))
print(crayons.green("╚═╝  ╚═╝     ╚═════╝  ╚═════╝    ╚═╝  \n"))
print(crayons.red("--------------------------------"))
print(crayons.blue(
    f'Fortnite Python bot made by brain and TJ. Version: {version}'))
print(crayons.blue('Join the discord: https://discord.gg/JwUgaua'))
print(crayons.red("--------------------------------"))


loop.run_until_complete(fortnitepy.start_multiple(to_run))
