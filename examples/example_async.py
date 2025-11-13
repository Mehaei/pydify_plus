import asyncio
import os
from dotenv import load_dotenv
from pydify_plus import AsyncClient

load_dotenv()

async def main():
    api_key = os.getenv("DIFY_API_KEY")
    base_url = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1")

    if not api_key:
        raise ValueError("DIFY_API_KEY environment variable not set")

    async with AsyncClient(base_url=base_url, api_key=api_key) as client:
        # Create a chat message
        chat_response = await client.chat.create_chat_message(
            model="claude-2",
            messages=[{"role": "user", "content": "Hello"}],
            conversation_id="123",
            user="test_user",
        )
        print("Chat response:", chat_response)

        # Create a dataset
        dataset_response = await client.dataset.create_dataset(name="My Dataset")
        print("Dataset response:", dataset_response)

if __name__ == "__main__":
    asyncio.run(main())