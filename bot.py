# bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from questions import quiz_data
from keyboards import generate_options_keyboard, get_start_keyboard
from database import get_quiz_index, update_quiz_index, save_result, get_result

# Кэш для подсчёта правильных ответов пользователя
user_scores = {}

async def right_answer(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer("✅ Верно!")

    # Увеличиваем счёт
    user_scores[user_id] = user_scores.get(user_id, 0) + 1

    current_index = await get_quiz_index(user_id)
    current_index += 1
    await update_quiz_index(user_id, current_index)

    if current_index < len(quiz_data):
        await send_question(callback.message, user_id)
    else:
        total = len(quiz_data)
        correct = user_scores.get(user_id, 0)
        await save_result(user_id, correct, total)
        await callback.message.answer(f"🎉 Квиз завершён!\nВаши результаты: {correct}/{total}")
        user_scores.pop(user_id, None)

async def wrong_answer(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_index = await get_quiz_index(user_id)
    correct_option = quiz_data[current_index]['correct_option']
    right_text = quiz_data[current_index]['options'][correct_option]
    await callback.message.answer(f"❌ Неправильно. Правильный ответ: {right_text}")

    current_index += 1
    await update_quiz_index(user_id, current_index)

    if current_index < len(quiz_data):
        await send_question(callback.message, user_id)
    else:
        total = len(quiz_data)
        correct = user_scores.get(user_id, 0)
        await save_result(user_id, correct, total)
        await callback.message.answer(f"🎉 Квиз завершён!\nВаши результаты: {correct}/{total}")
        user_scores.pop(user_id, None)

async def send_question(message: types.Message, user_id: int):
    index = await get_quiz_index(user_id)
    if index >= len(quiz_data):
        return

    question = quiz_data[index]
    right_answer_text = question['options'][question['correct_option']]
    kb = generate_options_keyboard(question['options'], right_answer_text)
    await message.answer(question['question'], reply_markup=kb)

async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в квиз по Python!", reply_markup=get_start_keyboard())

async def cmd_quiz(message: types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0  # сбрасываем счёт
    await update_quiz_index(user_id, 0)
    await message.answer("🚀 Начинаем квиз!")
    await send_question(message, user_id)

async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    result = await get_result(user_id)
    if result:
        correct, total = result
        await message.answer(f"📊 Ваш последний результат: {correct}/{total}")
    else:
        await message.answer("Вы ещё не проходили квиз.")

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_quiz, F.text == "Начать игру")
    dp.message.register(cmd_quiz, Command("quiz"))
    dp.message.register(cmd_stats, Command("stats"))
    dp.callback_query.register(right_answer, F.data == "right_answer")
    dp.callback_query.register(wrong_answer, F.data == "wrong_answer")