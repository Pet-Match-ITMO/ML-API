import json
from decouple import config
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class LLMSolver:
    def __init__(self):
        giga_key = config("SB_AUTH_DATA")
        self.llm = GigaChat(credentials=giga_key, model="GigaChat-Max", timeout=30, verify_ssl_certs=False)

    def is_animal_profile(self, post_text):
        system_prompt = 'Тебе дадут текст поста ВКонтакте, исходя из текста нужно определить, является ли пост анкетой животного из приюта.\
              Анкета должна содержать Имя/Кличку животного, сведения о прививках и описание характера животного.\
              Пост обязательно должен содержать контакты для связи с приютом, как минимум номер телефона.\
              В посте также обязательно должна быть фраза "... ищет дом"'
        user_prompt = f"Определи является ли данный текст анкетой животного: \"{post_text}\". Ответь только 1, если да; 0, если нет."
        response = self.solve(user_prompt=user_prompt, system_prompt=system_prompt)
        normalized_response = response.strip()

        if normalized_response == "1":
            return True
        else:
            return False

    def summarize(self, text) -> str:
        system_prompt = 'Тебе нужно сократить текст поста как минимум вдвое.\
            Все ключевые моменты и пункты необходимо оставить! В том числе контакты в конце поста и ссылки.'
        user_prompt = f"Суммаризируй следующий текст поста: {text}"
        response = self.solve(user_prompt=user_prompt, system_prompt=system_prompt)
        return response
    
    def solve(self, user_prompt, system_prompt) -> str:
        response = self.llm.stream(
            Chat(
                messages=[
                    Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                    Messages(role=MessagesRole.USER, content=user_prompt),
                ],
            )
        )

        generated_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                generated_response += chunk.choices[0].delta.content

        return generated_response
    
    def generate_pet_json_from_post(self, post_text: str) -> dict:
        """
        Генерирует JSON-данные о животном из текста поста с помощью LLM.
        Возвращает словарь с полями:
        age (объект: years, months, days), vaccinations, sterilization, health (объект: status, diseases, vaccinations),
        temperament (список характеристик и привычек), name, birth_place, grow_up_with, previous_owner,
        owner_requirements (список), sterilization
        """
        system_prompt = (
            "Ты — помощник для извлечения структурированных данных о животных из постов. "
            "Тебе будет дан текст поста о животном из приюта. "
            "Твоя задача — извлечь и вернуть данные в формате JSON строго по следующей схеме: "
            '{\n'
            '  "age": {"years": 0, "months": 0, "days": 0},\n'
            '  "vaccinations": true,\n'
            '  "sterilization": true,\n'
            '  "health": {\n'
            '    "status": "здоров",\n'
            '    "diseases": ["болезнь1", "болезнь2"],\n'
            '    "vaccinations": ["прививка1", "прививка2"]\n'
            '  },\n'
            '  "temperament": ["дружелюбный", "активный"],\n'
            '  "name": "Имя",\n'
            '  "birth_place": "город",\n'
            '  "grow_up_with": "семья/улица/другое",\n'
            '  "previous_owner": "владелец/приют" или null,\n'
            '  "owner_requirements": ["опытный", "без маленьких детей"],\n'
            '  "sterilization": true\n'
            '}'
            "\nЕсли данных нет — ставь null, пустую строку или пустой список. Не добавляй лишних полей. "
            "Поле previous_owner указывай только если известно, что животное было сдано от предыдущего хозяина или другого приюта, иначе null. "
            "Поле grow_up_with — где/с кем жило животное до приюта или где найдено. "
            "Поле temperament должно содержать список характеристик и привычек животного, а также отношение к людям. "
            "Поле owner_requirements — список требований к новому хозяину. "
            "Поле photos не включай. "
            "Если данных о плохом здоровье нет, пиши здоров/здоровая. "
            "Ответ должен быть только валидным JSON."
        )
        user_prompt = f"Извлеки данные из этого поста и верни только JSON: {post_text}"
        response = self.solve(user_prompt=user_prompt, system_prompt=system_prompt)
        try:
            return json.loads(response)
        except Exception:
            return {"error": "LLM did not return valid JSON", "raw": response}
