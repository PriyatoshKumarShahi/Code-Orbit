import asyncio
from app.services.verifier import verify_content

async def main():
    try:
        res = await verify_content("Free recharge link sab users ko free data de raha hai")
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
