import logging
import time
import json
from typing import Any, Generator, Optional

import openai
from openai import AzureOpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from src.domain.entities.models import Prompt


class OpenAIService:
    _logger: logging.Logger
    _azure_openai_client: AzureOpenAI

    def __init__(self, logger: logging.Logger, openai_client: AzureOpenAI) -> None:
        self._logger = logger
        self._azure_openai_client = openai_client

    def call_api(
        self,
        prompt: Prompt,
        user_msg: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> str:
        self._logger.debug(
            "call_api input {system_msg} {user_msg}",
            extra={"system_msg": prompt.system_message, "user_msg": user_msg},
        )
        wait_multiplier: int = 0
        while wait_multiplier < 4:
            wait_multiplier += 1
            self._logger.debug(f"call_api try {wait_multiplier}")
            try:
                response = self.get_completion(
                    prompt,
                    user_msg,
                    seed=seed,
                )

                self._logger.debug(
                    "call_api output {response}", extra={"response": response}
                )
                return json.loads(response.choices[0].message.content)

            except Exception as e:
                if isinstance(e, openai.RateLimitError):
                    if wait_multiplier > 3:
                        return ""
                    self._logger.error(
                        "Error in call_api using prompt: " + prompt.name + "\n" + str(e)
                    )
                    time.sleep(10 * wait_multiplier)
                elif isinstance(e, openai.BadRequestError):
                    self._logger.error(
                        "Error in call_api using prompt: " + prompt.name + "\n" + str(e)
                    )
                    return "Error: Vuelve a formular tu mensaje de manera más clara"
                else:
                    raise e

        return ""

    def get_completion(
        self,
        prompt: Prompt,
        user_msg: str | None,
        seed: Optional[int] = None,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        self._logger.debug(
            "get_completion input {prompt} {user_msg} {seed}",
            extra={"prompt": str(prompt), "user_msg": str(user_msg), "seed": str(seed)},
        )
        args: dict[str, Any] = {
            "messages": [{"role": "system", "content": prompt.system_message}]
            + [
                item
                for sublist in [
                    [
                        {
                            "role": "user",
                            "content": example.user_input,
                        },
                        {
                            "role": "assistant",
                            "content": example.chatbot_response,
                        },
                    ]
                    for example in prompt.few_shot_examples
                ]
                for item in sublist
            ]
            + [{"role": "user", "content": user_msg if user_msg is not None else ""}],
            "model": prompt.llm_model.name,  # type: ignore
            "temperature": prompt.temperature,
            "max_tokens": prompt.max_response_length,
            "top_p": prompt.top_probabilities,
            "frequency_penalty": prompt.frequency_penalty,
            "presence_penalty": prompt.presence_penalty,
            "stop": prompt.stop_sequences,
            "stream": prompt.stream,
        }
        if prompt.is_json:
            args["response_format"] = {"type": "json_object"}
        if seed:
            args["seed"] = seed

        return self._azure_openai_client.chat.completions.create(**args)  # type: ignore