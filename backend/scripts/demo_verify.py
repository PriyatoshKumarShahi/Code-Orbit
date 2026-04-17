import asyncio

from app.services.verifier import verify_content


async def main():
    sample = "Free recharge link sab users ko free data de raha hai, abhi click karo aur OTP dalo"
    result = await verify_content(sample)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
