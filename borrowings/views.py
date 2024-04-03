from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from telethon.sync import TelegramClient
import asyncio
from dotenv import dotenv_values

from borrowings.serializers import (
    BorrowingListCreateSerializer,
    BorrowingDetailSerializer,
)
from borrowings.models import Borrowing
from books_service.models import Book

ENV_VALUES = dotenv_values(".env")


async def helper(message_text: str) -> None:
    api_id = ENV_VALUES["API_ID"]
    api_hash = ENV_VALUES["API_HASH"]
    bot_token = ENV_VALUES["BOT_TOKEN"]
    group_id = int(ENV_VALUES["GROUP_ID"])

    async with TelegramClient("bot_session", api_id, api_hash) as client:
        await client.start(bot_token=bot_token)

        await client.send_message(group_id, message_text)


async def notification(message_text: str) -> None:
    await asyncio.sleep(0.1)
    await helper(message_text)


class BorrowingListCreateView(ListCreateAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        serializer.save(user=user)

        book_id = request.data.get("book")
        book = Book.objects.get(pk=book_id)

        self.perform_create(serializer)

        book.inventory -= 1
        book.save()

        asyncio.run(
            notification(
                f"book '{book.title}' has been borrowed by user: {request.user.email}"
            )
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowingDetailView(RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()


class BorrowingDestroyView(DestroyAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book = instance.book

        self.perform_destroy(instance)

        book.inventory += 1
        book.save()

        asyncio.run(
            notification(
                f"book '{book.title}' has been returned by user: {request.user.email}"
            )
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
