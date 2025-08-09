# utils/language_util.py
# English and Hindi language dictionaries

languages = {
    "en": {
        "start_message": "Welcome to DreamsMusic! Use /play <song name> to start.",
        "paused": "Playback paused.",
        "resumed": "Playback resumed.",
        "stopped": "Playback stopped.",
        "skipped": "Skipped current song.",
        "ended": "Playback ended.",
        "unknown_command": "Unknown command.",
        "no_query": "Please provide a song name or link.",
        "playing": "Now playing: {query}",
        "welcome_message": "Welcome {name} to the group!",
        "stats_message": "Uptime: {uptime}\nUsers: {users}\nChats: {chats}",
    },
    "hi": {
        "start_message": "DreamsMusic में आपका स्वागत है! /play <गाना नाम> से शुरू करें।",
        "paused": "प्लेबैक रुका।",
        "resumed": "प्लेबैक फिर से शुरू हुआ।",
        "stopped": "प्लेबैक बंद किया गया।",
        "skipped": "वर्तमान गाना छोड़ दिया गया।",
        "ended": "प्लेबैक समाप्त।",
        "unknown_command": "अज्ञात कमांड।",
        "no_query": "कृपया गाने का नाम या लिंक दें।",
        "playing": "अभी बज रहा है: {query}",
        "welcome_message": "{name} का समूह में स्वागत है!",
        "stats_message": "अपटाइम: {uptime}\nउपयोगकर्ता: {users}\nचैट्स: {chats}",
    }
}

def load_language(lang_code: str):
    return languages.get(lang_code, languages["en"])
