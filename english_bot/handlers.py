from functools import wraps
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, ReplyKeyboardRemove
from menu_struct import menu_options


import nltk
nltk.download('wordnet')
nltk.download('words')
from nltk.corpus import wordnet
from random import sample
from nltk.corpus import words

from translate import Translator
translator= Translator(to_lang="ru")


def send_typing_action(func):
    # typing
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


@send_typing_action
def start(update, context):
    first_name = update.message.chat.first_name
    opening_line = f"""Good day, {first_name}!\nI'm your virtual english teacher!"""
    update.message.reply_text(opening_line)
    show_menu(update, context)


def show_menu(update, context):
    keyboard = [
        [InlineKeyboardButton(menu_options['1']['option'], callback_data='1')],
        [InlineKeyboardButton(menu_options['2']['option'], callback_data='2'), InlineKeyboardButton(menu_options['3']['option'], callback_data='3')],
        [InlineKeyboardButton(menu_options['4']['option'], callback_data='4')],
        [InlineKeyboardButton(menu_options['5']['option'], callback_data='5')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select command:', reply_markup=reply_markup)


def menu_option(update, context):
    query = update.callback_query
    context.chat_data['option'] = [query.data]
    if query.data == '4':
        res = random_words_hand()
        s = "Random words\n"
        for w in res:
            translation = translator_hand(w)
            s += f"*{w}* \(RU:||{translation}||\)\n"
        query.message.reply_text(s, parse_mode='MarkdownV2')
        query.message.reply_text('Lets continue?', parse_mode='MarkdownV2')
        query.answer()
        show_menu(update, context)
        context.chat_data['option'] = ['']
    else:
        query.edit_message_text(text=menu_options[query.data]['reply'])
        query.answer()

@send_typing_action
def help(update, context):
    update.message.reply_text('Help message')

def translator_hand(text):
    return translator.translate(text)

def synonym_antonyms_hand(phrase, syn=True):
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    synonyms = list(set(synonyms))[:5]
    antonyms = list(set(antonyms))[:5]
    if syn:
        return '\n'.join(synonyms)
    else:
        return '\n'.join(antonyms)
    
def random_words_hand(n=3):
    rand_words = sample(words.words(), n)
    return rand_words

@send_typing_action
def message_reply(update, context):
    if 'option' in context.chat_data.keys():
        if context.chat_data['option'][0]=='1':
            text = update.message.text
            translation = translator_hand(text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=translation)
            followup_line = f"""*_Do you want to continue learning?_*"""
            update.message.reply_text(followup_line, parse_mode='MarkdownV2')
            show_menu(update, context)
            context.chat_data['option'] = ['']
        
        elif context.chat_data['option'][0]=='2':
            text = update.message.text
            result = synonym_antonyms_hand(text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=result)
            followup_line = f"""*_Do you want to continue learning?_*"""
            update.message.reply_text(followup_line, parse_mode='MarkdownV2')
            context.chat_data['option'] = ['']

        elif context.chat_data['option'][0]=='3':
            text = update.message.text
            result = synonym_antonyms_hand(text, False)
            context.bot.send_message(chat_id=update.effective_chat.id, text=result)
            followup_line = f"""*_Do you want to continue learning?_*"""
            update.message.reply_text(followup_line, parse_mode='MarkdownV2')
            context.chat_data['option'] = ['']

        elif context.chat_data['option'][0]=='5':
            text = update.message.text
            result = synonym_antonyms_hand(text, False)
            context.bot.send_message(chat_id=update.effective_chat.id, text=result)
            update.message.reply_text(
                "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
            )
            context.chat_data['option'] = ['']

        else:
            followup_line = f"""???"""
            update.message.reply_text(followup_line)
            show_menu(update, context)
    else:
        pass
