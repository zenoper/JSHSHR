from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import easyocr
import os

from app.states import Register

router = Router()
# Initialize EasyOCR reader for Uzbek and English
reader = easyocr.Reader(['en'])


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Register.photo)
    await message.answer("Iltimos, JSHSHR olish uchun rasm jo'nating.")
    # Open and send the photo using FSInputFile
    photo = FSInputFile("passport_example.jpg")
    await message.answer_photo(photo, caption="Qulaylik uchun, rasmda ko'rsatilganidek passportning faqatgina rasmi bor betini qirqib jo'nating.")


@router.message(F.photo, Register.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    
    # Download the photo
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_id + ".jpg"
    await message.bot.download_file(file.file_path, file_path)
    
    await message.answer("Rasmdan text o'qilyapti...")
    
    try:
        # Read text from image
        result = reader.readtext(file_path)
        
        # Extract all detected text 
        detected_text = ' '.join([text[1] for text in result])
        
        if detected_text:
            
            try:
                # Get the last part of text
                last_line = detected_text.split()[-1]
                jshshr = last_line[-16:-2]  # Get 14 characters from the end, excluding last 2
                if len(jshshr) == 14:
                    await message.answer(f"JSHSHR:\n\n<code>{jshshr}</code>", parse_mode="HTML")
                else:
                    await message.answer("Rasm ichidan JSHSHR topilmadi. Iltimos, sifatli rasm jo'nating.")
            except Exception as e:
                await message.answer("Rasm ichidan JSHSHR topilmadi. Iltimos, sifatli rasm jo'nating.")
        else:
            await message.answer("Rasm ichidan matn topilmadi. Iltimos, sifatli rasm jo'nating.")
            
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        await message.answer("Xatolik yuz berdi. Iltimos, boshqa rasm jo'nating.")
        
    finally:
        # Clean up - delete the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)