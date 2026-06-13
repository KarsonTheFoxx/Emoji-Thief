from disnake_plugins import Plugin
from disnake import Color, ui, MediaGalleryItem, ButtonStyle, MessageCommandInteraction
from disnake.ext import commands
from re import compile


PLUGIN = Plugin()


EMOJI_REGEX = compile(r"<(a?):(\w+):(\d+)>")

class EmojiDisplayMediaGallery(ui.MediaGallery):
    def __init__(self, items_to_add:list):
        items = []
        for item in items_to_add:
            items.append(MediaGalleryItem(item[1], description=item[0]))

        super().__init__(*items)

class SendErrorReportButton(ui.Button):
    def __init__(self, author_id):
        self.author_id = author_id
        super().__init__(style=ButtonStyle.grey, emoji="🪲", custom_id=f"send_error_report_button:{author_id}")

class EmojiStealerContainer(ui.Container):
    def __init__(self, media_gallery_items):
        if len(media_gallery_items) > 10:
            footer = ui.TextDisplay("-# Too many emojis! I can only steal the first 10!")
        else:
            footer = ui.TextDisplay("-# I think that's all of them! What a great heist!")

        components = [
            ui.TextDisplay(content=", ".join([emoji[0] for emoji in media_gallery_items[:9]])),
            EmojiDisplayMediaGallery(media_gallery_items[:9]),
            footer
        ]
        super().__init__(*components, accent_colour=Color.green())
        
@PLUGIN.message_command(name="Steal Emoji")
@commands.install_types(guild=False, user=True)
@commands.contexts(guild=True, bot_dm=True, private_channel=True)
async def steal_emoji(inter:MessageCommandInteraction):
    await inter.response.defer()
    regex_emoji_match = list(EMOJI_REGEX.finditer(inter.target.content))

    if regex_emoji_match:
        emoji_map = []

        for emoji_regex in regex_emoji_match:
            animated = emoji_regex.group(1)
            emoji_name = emoji_regex.group(2)
            emoji_id = emoji_regex.group(3)

            extension = "gif" if animated == "a" else "png"

            emoji_map.append((emoji_name, f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"))
        await inter.followup.send(
            components=[EmojiStealerContainer(emoji_map)]
        )
    else:
        await inter.followup.send("This message does not contain any custom emojis")

# @steal_emoji.on_error
# async def on_steal_emoji_error(inter:MessageCommandInteraction, error):
#     await inter.response.defer()
#     await inter.followup.send(f"{error} orccured")


print("Message_commands.py loaded")
setup, teardown = PLUGIN.create_extension_handlers()
