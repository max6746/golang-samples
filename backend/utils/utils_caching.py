"""Cache Content Helper Module"""

import datetime
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview import caching
from logger.logging import Logger
from config import Config

logger = Logger(__name__)


class GeminiContentCache:
    """cached content object"""

    def __init__(
        self,
        model_name: str = "gemini-1.5-pro-001",
        system_instruction: str = None,
        cache_id: str = None,
        ttl_minutes: int = 60,
    ) -> None:
        self.model_name = model_name
        self.system_instruction = system_instruction
        if self.system_instruction is None:
            self.system_instruction = Config.DEFAULT_SYSTEM_INSTRUCTION
        self.cache_id = cache_id
        self.ttl_minutes = ttl_minutes

    def create_cached_content(self, contents: list[Part]) -> str:
        """creates cache content, returns cache_id"""
        cached_content = caching.CachedContent.create(
            model_name=self.model_name,
            system_instruction=self.system_instruction,
            contents=contents,
            ttl=datetime.timedelta(minutes=self.ttl_minutes),
        )
        self.cache_id = cached_content.name
        return self.cache_id

    def prompt_cached_content(self, prompt: str) -> str:
        """prompt cached content, returns generated text"""
        if not self.cache_id:
            raise ValueError("missing cache_id")
        cached_content = caching.CachedContent(cached_content_name=self.cache_id)

        model = GenerativeModel.from_cached_content(cached_content=cached_content)
        response = model.generate_content(prompt)
        return response.text

    def prompt_docs(
        self,
        prompt: str,
        doc_cache_id_map: dict,
        doc_names: list[str],
        contents: list[Part] = None,
    ):
        """gets cached content text of provided doc_names,
        doc_cache_id_map in doc_names:cache_id pair,
        handles already cached data"""
        set_docs = frozenset(doc_names)

        if doc_cache_id_map.get(set_docs):
            self.cache_id = doc_cache_id_map[set_docs]
        else:
            logger.debug(f"Creating cache for docs {set_docs}")
            self.cache_id = self.create_cached_content(contents)
            doc_cache_id_map[set_docs] = self.cache_id
        logger.debug(f"docs {set_docs} cache id {self.cache_id}")

        cache_response = self.prompt_cached_content(prompt)
        logger.debug(f"cache_id {self.cache_id} response {cache_response}")
        return cache_response
