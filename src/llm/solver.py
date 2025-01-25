from decouple import config
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class LLMSolver:
    def __init__(self):
        giga_key = config("SB_AUTH_DATA")
        self.llm = GigaChat(credentials=giga_key, model="GigaChat", timeout=30, verify_ssl_certs=False)

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
