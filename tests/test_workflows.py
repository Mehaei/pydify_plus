import pytest
from httpx import Response
from pydify_plus import AsyncClient as DifyAsyncClient


@pytest.mark.asyncio
async def test_execute_workflow(respx_mock):
    respx_mock.post("/v1/workflows/wf_1/execute").mock(return_value=Response(200, json={"execution_id": "exe_1"}))
    async with DifyAsyncClient(base_url="http://localhost", api_key="test") as client:
        resp = await client.workflows.execute("wf_1", inputs={"a": 1})
        assert resp["execution_id"] == "exe_1"