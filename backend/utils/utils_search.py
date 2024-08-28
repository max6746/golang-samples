from google.cloud import discoveryengine_v1beta as discoveryengine
from google.cloud.discoveryengine_v1beta.services.search_service.pagers import (
    SearchPager,
)
from google.cloud import aiplatform_v1

from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class VertexSearch:
    def __init__(
        self,
        project_id: str,
        datastore_location: str,
        serving_config_id: str,
        datastore_id: str,
        ismultiturn: bool = False,
    ) -> None:
        # Global configurations
        self.project_id = project_id

        # Vertex Search configurations
        self.datastore_location = datastore_location
        self.serving_config_id = serving_config_id
        self.datastore_id = datastore_id

        if ismultiturn:
            self.converse_client = discoveryengine.ConversationalSearchServiceClient()
        else:
            self.search_client = discoveryengine.SearchServiceClient()

    def vertexai_search_oneturn(
        self,
        search_query: str,
        include_content_spec: bool = True,
        include_citations: bool = True,
        summary_result_count: int = 3,
        return_snippet: bool = True,
        page_size: int = 20,
        search_filter: str = "",
        model_version: str = "preview",
    ) -> SearchPager:
        """
        Args:
            search_query: str
                The search query.
            return_snippet: bool
                Whether to return the snippet of the document. Default is True.
            summary_result_count: int
                The number of summary results to return. Default is 3.
            include_citations: bool
                Whether to include citations. Default is True.

        Returns:
            search_service.pagers.SearchPager
                Response message for [SearchService.Search] method.

                Iterating over this object will yield results and resolve
                additional pages automatically.
        """
        serving_config = self.search_client.serving_config_path(
            project=self.project_id,
            location=self.datastore_location,
            data_store=self.datastore_id,
            serving_config=self.serving_config_id,
        )

        content_spec = None
        if include_content_spec:
            snippet_spec = discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=return_snippet
            )
            summary_spec = discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                summary_result_count=summary_result_count,
                include_citations=include_citations,
                model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                    version=model_version,
                ),
            )
            content_spec = discoveryengine.SearchRequest.ContentSearchSpec(
                snippet_spec=snippet_spec, summary_spec=summary_spec
            )

        request = discoveryengine.SearchRequest(
            content_search_spec=content_spec,
            serving_config=serving_config,
            query=search_query,
            page_size=page_size,
            filter=search_filter,
        )

        response = self.search_client.search(request)

        return response

    def vertexai_search_multiturn(
        self,
        search_query: str,
        conversation_id: str,
        datastore_id: str,
        include_citations: bool = True,
        summary_result_count: int = 5,
        model_version: str = "preview",
    ) -> discoveryengine.ConverseConversationResponse:
        """Searches for documents on Vertex AI Search using a conversational
        interface.

        Args:
            search_query (str):
                User query
            conversation_id (str):
                Vertex AI Search conversation identifier
            include_citations (bool):
                Include or not citations
                Default: True
            summary_result_count (int):
                Number of summary results to return
                Default: 5
            datastore_id (str):
                Datastore identifier

        Returns:
            (discoveryengine.ConverseConversationResponse)
            Response for the query.
        """
        serving_config = self.converse_client.serving_config_path(
            project=self.project_id,
            location=self.datastore_location,
            data_store=datastore_id,
            serving_config=self.serving_config_id,
        )

        summary_spec = discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            include_citations=include_citations,
            summary_result_count=summary_result_count,
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version=model_version,
            ),
        )

        request = discoveryengine.ConverseConversationRequest(
            name=conversation_id,
            query=discoveryengine.TextInput(input=search_query),
            serving_config=serving_config,
            summary_spec=summary_spec,
            # search_filter=search_filter,  # Uncomment when available in Proto
        )

        response = self.converse_client.converse_conversation(request)

        return response


class VectorSearch:
    """
    Utility module for Vertex AI Vector Search
    """

    def __init__(self, project_number: str, vector_api_endpoint: str) -> None:
        """

        Args:
            project_number (str): Project Number
            vector_api_endpoint (str): Vector API Endpoint
        """

        self.project_number = project_number

        self.match_client = aiplatform_v1.MatchServiceClient(
            client_options={"api_endpoint": vector_api_endpoint}
        )

    def find_neighbor(
        self,
        feature_vector: list,
        index_endpoint_id: str,
        deployed_index_id: str,
        datapoint_id: str = "0",
        neighbor_count: int = 10,
    ) -> aiplatform_v1.FindNeighborsResponse:
        """Find Nearest Neighbour in Vector

        Args:
            feature_vector (list): Feature Vectore
            index_endpoint_id (str): Index Endpoint ID
            deployed_index_id (str): Deployed Index ID
            datapoint_id (str, optional): . Defaults to "0".
            neighbor_count (int, optional):. Defaults to 10.

        Returns:
            aiplatform_v1.FindNeighborsResponse: _description_
        """

        query = aiplatform_v1.FindNeighborsRequest.Query(
            datapoint=aiplatform_v1.IndexDatapoint(
                datapoint_id=datapoint_id, feature_vector=feature_vector
            ),
            neighbor_count=neighbor_count,
        )

        request = aiplatform_v1.FindNeighborsRequest(
            index_endpoint=f"projects/{self.project_number}/locations/us-central1/"
            f"indexEndpoints/{index_endpoint_id}",
            deployed_index_id=deployed_index_id,
            return_full_datapoint=False,
            queries=[query],
        )

        return self.match_client.find_neighbors(request)
