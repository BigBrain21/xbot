import fortnitepy
import json
import os
import requests
import functools
import random
import time
import crayons
import threading
import sys
from datetime import datetime
import aiohttp


version = "1.7"


filename = 'device_auths.json'
try:
    with open("config.json") as f:
        data = json.load(f)
except:
    a = input("What is the username of the bot's account?: ")
    b = input("What is the password of the bot's account?: ")
    with open("config.json", "w") as f:
        json.dump({'email': a, 'password': b, 'friendaccept': True, 'defaultskin': 'renegade raider', 'defaultlevel': 123,
                   'defaultbackpack': 'black shield', 'defaultpickaxe': "raider's revenge", 'admin': '', 'platform': 'WIN'}, f, indent=4, sort_keys=False)
    data = {'email': a, 'password': b, 'friendaccept': True, 'defaultskin': 'renegade raider', 'defaultlevel': 123,
            'defaultbackpack': 'black shield', 'defaultpickaxe': "raider's revenge", 'admin': '', 'platform': 'WIN'}

email = data["email"]
password = data["password"]
default_level = data["defaultlevel"]


class default_cosmetics:
    def __init__(self):
        self.default_skin = "CID_028_Athena_Commando_F"
        self.default_pickaxe = "Pickaxe_Lockjaw"
        self.defaultbackpack = "BID_004_BlackKnight"


async def set_and_update_party_prop(schema_key: str, new_value) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.patch(updated=prop)


async def set_and_update_member_prop(schema_key: str, new_value) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.me.patch(updated=prop)


class command_handle:
    def __init__(self, data):
        self.data = data

    async def handle(self, message):
        command = message.content.split(" ", 1)
        time_c = datetime.now().strftime("%H:%M:%S")
        await self.data[command[0]](message, command, time_c)


class MyClient(fortnitepy.Client):
    def __init__(self):
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
        default.default_skin = requests.get(
            f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={data['defaultskin']}&backendType=AthenaCharacter").json()[0]["id"]
        default.defaultbackpack = requests.get(
            f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={data['defaultbackpack']}&backendType=AthenaBackpack").json()[0]["id"]
        default.default_pickaxe = requests.get(
            f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={data['defaultpickaxe']}&backendType=AthenaPickaxe").json()[0]["id"]
        print(crayons.green("\n\n██╗  ██╗     ██████╗  ██████╗ ████████╗"))
        print(crayons.green("╚██╗██╔╝     ██╔══██╗██╔═══██╗╚══██╔══╝"))
        print(crayons.green(" ╚███╔╝█████╗██████╔╝██║   ██║   ██║   "))
        print(crayons.green(" ██╔██╗╚════╝██╔══██╗██║   ██║   ██║   "))
        print(crayons.green("██╔╝ ██╗     ██████╔╝╚██████╔╝   ██║   "))
        print(crayons.green("╚═╝  ╚═╝     ╚═════╝  ╚═════╝    ╚═╝  \n"))
        print(crayons.red("--------------------------------"))
        print(crayons.blue(
            f'Fortnite Python bot made by mistxbrain and TJ. Version: {version}'))
        print(crayons.blue('Join the discord: https://discord.gg/6sMKGeg'))
        print(crayons.green(f'Bot ready as {self.user.display_name}'))
        print(crayons.red("--------------------------------"))
        for a in list(client.pending_friends.values()):
            if a.incoming:
                if data["friendaccept"]:
                    await a.accept()
                    now = datetime.now()
                    time_b = now.strftime("%H:%M:%S")
                    print(crayons.blue(f"[X-Bot] [{time_b}]: ") + crayons.green(
                        f"Accepted friend request from {a.display_name}"))
                else:
                    await a.decline()

    async def event_friend_request(self, request):
        if data["friendaccept"]:
            await request.accept()

    async def event_party_invite(self, invite):
        now = datetime.now()
        time_b = now.strftime("%H:%M:%S")
        print(crayons.blue(f"[X-Bot] [{time_b}]: ") + crayons.green(
            f"Recieved party invite from {invite.sender.display_name}"))
        await invite.accept()
        print(crayons.blue(f"[X-Bot] [{time_b}]: ") + crayons.green(
            f"Joined {invite.sender.display_name}'s party"))
        await reset()

    async def event_party_member_join(self, member):
        if client.party.member_count == 2:
            await reset()

    async def event_friend_message(self, message):
        now = datetime.now()
        time_c = now.strftime("%H:%M:%S")
        print(crayons.blue(
            f"[{message.author.display_name}] [{time_c}]: ") + crayons.magenta(message.content))
        # try:
        await bot_class.handle(message)
        """
        except:
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.red(f"Unknown command '{message.content}'"))"""


async def skin(message, msg, time_c):
    response = requests.get(
        f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaCharacter").json()
    if response == []:
        await message.reply("Please enter a valid skin name.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red("Please enter a valid skin."))
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_outfit(id)
            await message.reply(f"Skin set to {id}")
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.green(f"Skin set to {id}"))
        except:
            await message.reply("An Unknown error occured.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red("An unknown error occured."))


async def emote(message, msg, time_c):
    response = requests.get(
        f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaDance").json()
    if response == []:
        await message.reply("Please enter a valid emote.")
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_emote(id)
            await message.reply(f"Emote set to {id}")
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.green(f"Emote set to {id}"))
        except:
            await message.reply("An Unknown error occured.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red(f"An unknown error occured."))


async def backpack(message, msg, time_c):
    response = requests.get(
        f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaBackpack").json()
    if response == []:
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red(f"Please enter a valid backpack."))
        await message.reply("Please enter a valid backpack.")
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_backpack(id)
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.green(f"Backpack set to set to {id}"))
            await message.reply(f"Backpack set to {id}")
        except:
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red(f"An unknown error occured."))
            await message.reply("An unknown error occured.")


async def level(message, msg, time_c):
    try:
        await client.party.me.set_banner(season_level=int(msg[1]))
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Level set to {msg[1]}"))
        await message.reply(f"Level set to {msg[1]}")
    except:
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red(f"Enter a valid number."))
        await message.reply("Enter a valid number.")


async def henchman(message, msg, time_c):
    if msg[1].lower() == "ghost":
        await client.party.me.set_outfit("CID_707_Athena_Commando_M_HenchmanGood")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Outfit set to ghost henchman."))
        await message.reply("Outfit set to ghost henchman.")
    elif msg[1].lower() == "shadow":
        await client.party.me.set_outfit("cid_npc_athena_commando_m_henchmanbad")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Outfit set to shadow henchman."))
        await message.reply("Outfit set to shadow henchman.")


async def leave(message, msg, time_c):
    await client.party.me.leave()
    await message.reply("Left the party.")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Left the party."))


async def battlepass(message, msg, time_c):
    try:
        await client.party.me.set_battlepass_info(has_purchased=True, level=int(msg[1]))
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Battlepass level set to: {msg[1]}"))
        await message.reply("Battlepass info updated.")
    except:
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red(f"Please enter a valid level."))
        await message.reply("Please enter a valid level.")


async def pinkghoul(message, msg, time_c):
    variants = client.party.me.create_variants(material=3)
    await client.party.me.set_outfit("CID_029_Athena_Commando_F_Halloween", variants=variants)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Outfit set to the pink ghoul trooper."))
    await message.reply("Outfit set to the pink ghoul trooper.")


async def stop(message, msg, time_c):
    await client.party.me.clear_emote()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Emote cleared."))
    await message.reply("Emote cleared.")


async def purpleskull(message, msg, time_c):
    variants = client.party.me.create_variants(clothing_color=1)
    await client.party.me.set_outfit("cid_030_athena_commando_m_halloween", variants=variants)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Outfit set to the purple skull trooper."))
    await message.reply("Outfit set to the purple skull trooper.")


async def checkeredrenegade(message, msg, time_c):
    variants = client.party.me.create_variants(material=2)
    await client.party.me.set_outfit("CID_028_Athena_Commando_F", variants=variants)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Outfit set to the checkered renegade raider."))
    await message.reply("Outfit set to the checkered renegade raider.")


async def copy(message, msg, time_c):
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
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Copied their loadout!"))
        await message.reply("Copied their loadout!")
    except:
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Please enter a valid party member."))
        await message.reply("Please enter a valid party member.")


async def ready(message, msg, time_c):
    await client.party.me.set_ready(fortnitepy.enums.ReadyState.READY)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Ready"))
    await message.reply("Ready")


async def unready(message, msg, time_c):
    await client.party.me.set_ready(fortnitepy.enums.ReadyState.NOT_READY)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Unready"))
    await message.reply("Unready")


async def sitout(message, msg, time_c):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Sitting out"))
    await message.reply("Sitting Out")


async def rare(message, msg, time_c):
    await client.party.me.set_outfit("CID_028_Athena_Commando_F")
    await client.party.me.set_backpack("BID_004_BlackKnight")
    await client.party.me.set_pickaxe("Pickaxe_Lockjaw")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Set to a rare loadout."))
    await message.reply("Set to a rare loadout.")


async def random_a(message, msg, time_c):
    allcos = requests.get(
        url="https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaCharacter").json()
    length = len(allcos)
    cid = allcos[random.randint(1, length)]["id"]
    allcos = requests.get(
        url="https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaBackpack").json()
    length = len(allcos)
    bid = allcos[random.randint(1, length)]["id"]
    allcos = requests.get(
        url="https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=full&backendType=AthenaPickaxe").json()
    length = len(allcos)
    pid = allcos[random.randint(1, length)]["id"]
    await client.party.me.set_backpack(bid)
    await client.party.me.set_outfit(cid)
    await client.party.me.set_pickaxe(pid)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Randomized the loadout!"))
    await message.reply("Randomized the loadout.")


async def status(message, msg, time_c):
    await client.set_status(status=msg[1])
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Status set to {msg[1]}"))
    await message.reply("Status set.")


async def loserfruit(message, msg, time_c):
    await client.party.me.set_outfit("CID_764_Athena_Commando_F_Loofah")
    await client.party.me.set_backpack("BID_527_Loofah")
    await client.party.me.set_emote("EID_Loofah")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
        f"Set to loserfruit's loadout! (note: this can only be seen on console)"))
    await message.reply("Set to loserfruit's loadout!")


async def goldenpeely(message, msg, time_c):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=4)
    await client.party.me.set_outfit("CID_701_Athena_Commando_M_BananaAgent", variants=variants, enlightenment=(2, 350))
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Outfit set to golden peely."))
    await message.reply("Outfit set to golden peely.")


async def mintyelf(message, msg, time_c):
    variants = fortnitepy.ClientPartyMember.create_variants(material=2)
    await client.party.me.set_outfit("CID_051_Athena_Commando_M_HolidayElf", variants=variants)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Outfit set to minty elf"))
    await message.reply("Outfit set to minty elf.")


async def femalehenchman(message, msg, time_c):
    if msg[1].lower() == "ghost":
        await client.party.me.set_outfit("CID_NPC_Athena_Commando_F_HenchmanSpyGood")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Outfit set to female ghost henchman"))
        await message.reply("Outfit set to the female ghost henchman")
    elif msg[1].lower() == "shadow":
        await client.party.me.set_outfit("CID_NPC_Athena_Commando_F_HenchmanSpyDark")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Outfit set to female shadow henchman"))
        await message.reply("Outfit set to the female ghost henchman")


async def goldenskye(message, msg, time_c):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=4)
    await client.party.me.set_outfit("CID_690_Athena_Commando_F_Photographer", variants=variants, enlightenment=(2, 300))
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Skin set to golden skye"))
    await message.reply("Skin set to golden skye")


async def point(message, msg, time_c):
    await client.party.me.set_emote("EID_IceKing")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Pointing!"))
    await message.reply("Pointing!")


async def vbucks(message, msg, time_c):
    await client.party.me.set_emote("EID_TakeTheL")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Lol"))
    await message.reply("Noob")


async def nobackpack(message, msg, time_c):
    await client.party.me.clear_backpack()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Backpack cleared"))
    await message.reply("Backpack cleared")


async def invite(message, msg, time_c):
    await message.author.invite()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Invite sent!"))
    await message.reply("Invite sent")


async def join(message, msg, time_c):
    await message.author.join_party()
    await reset()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Joined {message.author.display_name}'s party'"))
    await message.reply("Joined")


async def reset_c(message, msg, time_c):
    await reset()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Reset my loadout"))
    await message.reply("Reset my loadout")


async def hide(message, msg, time_c):
    if client.party.me.leader:
        if msg[1] != "all":
            user = await client.fetch_profile_by_display_name(msg[1])
            member = client.party.members.get(user.id)
            if member is not None:
                raw_squad_assignments = client.party.meta.get_prop(
                    'Default:RawSquadAssignments_j')["RawSquadAssignments"]
                for player in raw_squad_assignments:
                    if player['memberId'] == member.id:
                        raw_squad_assignments.remove(player)
                await set_and_update_party_prop('Default:RawSquadAssignments_j', {'RawSquadAssignments': raw_squad_assignments})
            else:
                await message.reply(f'Couldn\'t find a user with name: {msg[1]}.')
                print(crayons.blue(
                    f"[X-Bot] [{time_c}]: ") + crayons.red(f"Couldn't find a user with the name {msg[1]}"))
        else:
            await set_and_update_party_prop(
                'Default:RawSquadAssignments_j', {
                    'RawSquadAssignments': [{'memberId': client.user.id, 'absoluteMemberIdx': 1}]
                }
            )
            await message.reply('Hid everyone.')
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.green(f"Hid everyone"))
    else:
        await message.reply("I cannot hide anyone unless I am party leader.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.red(
            f"Unable to hide everyone (I'm not party leader)"))


async def unhide(message, msg, time_c):
    if msg[1] != "all":
        user = await client.fetch_profile_by_display_name(msg[1])
        member = client.party.members.get(user.id)
        if member is None:
            await message.reply("Unable to find user.")
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.red(f"Couldn't find the specified user."))
        else:
            await member.promote()
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.green(f"Unhid all and set {msg[1]} party leader."))
            await message.reply("Unhid everybody")
    else:
        user = await client.fetch_profile_by_display_name(message.author.display_name)
        member = client.party.members.get(user.id)
        await member.promote()
        await message.reply("Unhid all")
        print(crayons.blue(
            f"[X-Bot] [{time_c}]: ") + crayons.green(f"Unhid all"))


async def gift(message, msg, time_c):
    await client.party.me.set_emote("EID_MakeItRain")
    time.sleep(2)
    await client.party.me.set_emote("EID_TakeTheL")
    time.sleep(2)
    await client.party.me.clear_emote()
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Syke"))
    await message.reply("Syke")


async def friend(message, msg, time_c):
    if message.author.display_name == data["admin"]:
        try:
            user = await client.fetch_profile_by_display_name(msg[1])
            await client.add_friend(user.id)
            await message.reply(f"Added user {user.id}")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.green(f"Added user {user.id}"))
        except:
            await message.reply(f"User {msg[1]} does not exist")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red(f"User {msg[1]} does not exist"))


async def unfriend(message, msg, time_c):
    if message.author.display_name == data["admin"]:
        try:
            user = await client.fetch_profile_by_display_name(msg[1])
            await client.remove_or_decline_friend(user.id)
            await message.reply(f"Removed friend {user.id}")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.green(f"Removed friend {user.id}"))
        except:
            await message.reply(f"User {msg[1]} does not exist or is not friends")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"User {msg[1]} does not exist or is not friends"))


async def promote(message, msg, time_c):
    if message.author.display_name == data["admin"]:
        user = await client.fetch_profile_by_display_name(msg[1])
        member = client.party.members.get(user.id)
        await member.promote()
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Promoted user {user.id}"))


async def vbuck_man(message, msg, time_c):
    if msg[1].lower() == "man":
        await client.party.me.set_outfit("CID_129_Athena_Commando_M_Deco")
        await client.party.me.set_backpack("BID_069_DecoMale")
        await client.party.me.set_emote("EID_MakeItRain")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.green(f"Outfit set to vbuck man"))
        await message.reply("Outfit set to vbuck man")


async def bp(message, msg, time_c):
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
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Done"))
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
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(f"Done"))
        await message.reply("Done")


async def hatlessrecon(message, msg, time_c):
    variants = fortnitepy.ClientPartyMember.create_variants(parts=2)
    await client.party.me.set_outfit("CID_022_Athena_Commando_F", variants=variants)


async def friendaccept(message, msg, time_c):
    if data["admin"] == message.author.display_name:
        if msg[1].lower() == "false":
            data["friendaccept"] = False
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
                print(crayons.blue(
                    f"[X-Bot] [{time_c}]: ") + crayons.green(f"Accept friend requests set to false"))
                await message.reply("Accept friend requests set to false")
        elif msg[1].lower() == "true":
            data["friendaccept"] = "true"
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
                print(crayons.blue(
                    f"[X-Bot] [{time_c}]: ") + crayons.green(f"Accept friend requests set to true"))
                await message.reply("Accept friend requests set to true")


async def hologram(message, msg, time_c):
    await client.party.me.set_outfit("CID_VIP_Athena_Commando_M_GalileoGondola_SG")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Skin set to the hologram skin"))


async def pickaxe(message, msg, time_c):
    response = requests.get(
        f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaPickaxe").json()
    if response == []:
        await message.reply("Please enter a valid pickaxe name.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red("Please enter a valid pickaxe."))
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_pickaxe(id)
            await message.reply(f"Pickaxe set to {id}")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.green(f"Pickaxe set to {id}"))
        except:
            await message.reply("An Unknown error occured.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red("An unknown error occured."))


async def emoji(message, msg, time_c):
    response = requests.get(
        f"https://benbotfn.tk/api/v1/cosmetics/br/search/all?lang=en&searchLang=en&matchMethod=contains&name={msg[1]}&backendType=AthenaEmoji").json()
    if response == []:
        await message.reply("Please enter a valid emoji name.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red("Please enter a valid emoji."))
    else:
        try:
            id = response[0]["id"]
            await client.party.me.set_emoji(id)
            await message.reply(f"Emoji set to {id}")
            print(crayons.blue(
                f"[X-Bot] [{time_c}]: ") + crayons.green(f"Emoji set to {id}"))

        except:
            await message.reply("An Unknown error occured.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
                  crayons.red("An unknown error occured."))


async def banner(message, msg, time_c):
    await client.party.me.set_banner(msg[1])
    await message.reply(f"Banner set to {msg[1]}")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Banner set to {msg[1]}"))


async def playlist(message, msg, time_c):
    await client.party.set_playlist(playlist=msg[1], region=fortnitepy.Region.EUROPE)


async def maskedfade(message, msg, time_c):
    variants = fortnitepy.ClientPartyMember.create_variants(progressive=3)
    await client.party.me.set_outfit("CID_777_Athena_Commando_M_RacerZero", variants=variants)
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Skin set to masked fade"))
    await message.reply("Skin set to masked fade")


async def variants(message, msg, time_c):
    content = msg[1].split(" ", 1)
    if content[0].isdigit():
        code = requests.get(
            f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=contains&name={content[1]}").json()
        type_v = code["variants"][0]["channel"].lower()
        variants = fortnitepy.ClientPartyMember.create_variants(
            **{type_v: content[0]}
        )
        if "cid" in code["id"].lower():
            await client.party.me.set_outfit(code["id"], variants=variants)
            await message.reply(f"Outfit set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Outfit set to {code['id']} with the {content[0]} variant."))
        elif "bid" in code["id"].lower():
            await client.party.me.set_backpack(code["id"], variants=variants)
            await message.reply(f"Backpack set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Backpack set to {code['id']} with the {content[0]} variant."))
        elif "pickaxe" in code["id"].lower():
            await client.party.me.set_pickaxe(code["id"], variants=variants)
            await message.reply(f"Pickaxe set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Pickaxe set to {code['id']} with the {content[0]} variant."))
    else:
        await message.reply("Please enter the command in a valid syntax.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red("Please enter the command in a valid syntax."))


async def style(message, msg, time_c):
    content = msg[1].split(" ", 2)
    if content[0].isdigit():
        code = requests.get(
            f"https://benbotfn.tk/api/v1/cosmetics/br/search?lang=en&searchLang=en&matchMethod=full&name={content[2]}").json()
        type_v = content[1]
        variants = fortnitepy.ClientPartyMember.create_variants(
            **{type_v: content[0]}
        )
        if "cid" in code["id"].lower():
            await client.party.me.set_outfit(code["id"], variants=variants)
            await message.reply(f"Outfit set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Outfit set to {code['id']} with the {content[0]} variant."))
        elif "bid" in code["id"].lower():
            await client.party.me.set_backpack(code["id"], variants=variants)
            await message.reply(f"Backpack set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Backpack set to {code['id']} with the {content[0]} variant."))
        elif "pickaxe" in code["id"].lower():
            await client.party.me.set_pickaxe(code["id"], variants=variants)
            await message.reply(f"Pickaxe set to {code['id']} with the {content[0]} variant.")
            print(crayons.blue(f"[X-Bot] [{time_c}]: ") + crayons.green(
                f"Pickaxe set to {code['id']} with the {content[0]} variant."))
    else:
        await message.reply("Please enter the command in a valid syntax.")
        print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
              crayons.red("Please enter the command in a valid syntax."))


async def eternalknight(message, msg, time_c):
    variants = variants = fortnitepy.ClientPartyMember.create_variants(
        progressive=2, material=2)
    await client.party.me.set_outfit("CID_767_Athena_Commando_F_BlackKnight", variants=variants, enlightenment=(3, 160))
    await message.reply(f"Skin set to max eternal knight.")
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Skin set to max eternal knight."))


async def threads(message, msg, time_c):
    print(crayons.blue(f"[X-Bot] [{time_c}]: ") +
          crayons.green(f"Thread count: {threading.active_count()}"))
    await message.reply(f"Thread count: {threading.active_count()}")


bot_class = command_handle({"!skin": skin, "!emote": emote, "!backpack": backpack, "!level": level, "!henchman": henchman, "!leave": leave, "!battlepass": battlepass, "!pinkghoul": pinkghoul, "!stop": stop, "!purpleskull": purpleskull, "!copy": copy, "!ready": ready, "!unready": unready, "!sitout": sitout,
                            "!random": random_a, "!status": status, "!loserfruit": loserfruit, "!goldenpeely": goldenpeely, "!mintyelf": mintyelf, "!femalehenchman": femalehenchman, "!goldenskye": goldenskye, "!point": point, "!vbucks": vbucks, "!nobackpack": nobackpack, "!invite": invite, "!join": join, "!reset": reset_c, "!hide": hide, "!unhide": unhide, "!gift": gift, "!friend": friend, "!unfriend": unfriend, "!promote": promote, "!vbuck": vbuck_man, "!bp": bp, "!hatlessrecon": hatlessrecon, "!friendaccept": friendaccept, "!hologram": hologram, "!pickaxe": pickaxe, "!emoji": emoji, "!banner": banner, "!playlist": playlist, "!maskedfade": maskedfade, "!variants": variants, "!style": style, "!eternalknight": eternalknight, "!threads": threads})
default = default_cosmetics()


async def reset():
    await client.party.me.set_outfit(default.default_skin)
    await client.party.me.set_banner(season_level=default_level)
    await client.party.me.set_backpack(default.defaultbackpack)
    await client.party.me.set_pickaxe(default.default_pickaxe)

client = MyClient()
client.run()
    