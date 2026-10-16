
"""SnackStack CLI with text and voice interaction."""

import argparse
import uuid

from langgraph.types import Command, Overwrite

from SnackStack.config import get_logger
from SnackStack.graph import graph
from SnackStack.Voice.recorder import VoiceRecorder
from SnackStack.Voice.speaker import VoiceSpeaker

logger = get_logger("main")


class SnackStackAssistant:
    """Run SnackStack conversations using the existing LangGraph."""

    def __init__(self, voice_mode: bool = False, voice_out: bool = False):
        self.thread_id = str(uuid.uuid4())
        self.voice_mode = voice_mode
        self.voice_out = voice_out

        self.recorder = VoiceRecorder() if voice_mode else None
        self.speaker = VoiceSpeaker() if (voice_mode or voice_out) else None

    @property
    def config(self):
        return {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

    def ask(self, question: str) -> str:
        """Send a question to LangGraph and handle interruptions."""

        try:
            result = graph.invoke(
                {
                    "user_query": question,
                    "agent_results": Overwrite([]),
                },
                config=self.config,
            )

            while True:
                snapshot = graph.get_state(self.config)

                pending = [
                    interrupt_item
                    for task in snapshot.tasks
                    for interrupt_item in task.interrupts
                ]

                if not pending:
                    break

                for interrupt_item in pending:
                    prompt = str(interrupt_item.value)
                    print(f"\nSnackStack needs more information: {prompt}")

                    if self.voice_mode:
                        print("Please answer using your microphone.")
                        answer = self.recorder.listen()
                    else:
                        answer = input("You: ").strip()

                    if not answer:
                        print("I didn't receive an answer. Please try again.")
                        answer = (
                            self.recorder.listen()
                            if self.voice_mode
                            else input("You: ").strip()
                        )

                    result = graph.invoke(
                        Command(resume=answer),
                        config=self.config,
                    )

            return result.get(
                "final_answer",
                "Sorry, I couldn't generate a response.",
            )

        except Exception as exc:
            logger.exception("Conversation failed.")
            return f"Sorry, something went wrong: {exc}"

    def reset(self):
        """Start a new conversation thread."""

        self.thread_id = str(uuid.uuid4())
        print("SnackStack: Conversation reset.")

    def chat(self):
        """Run the text-based conversation loop."""

        print("\nSnackStack is ready!")
        print("Ask about the menu or track your order.")
        print("Type 'reset' to start a new conversation.")
        print("Type 'quit' to exit.\n")

        while True:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in ("quit", "exit"):
                print("SnackStack: Goodbye!")
                break

            if question.lower() == "reset":
                self.reset()
                continue

            answer = self.ask(question)
            print(f"\nSnackStack: {answer}\n")

            if self.voice_out and self.speaker:
                self.speaker.speak(answer)

    def voice_chat(self):
        """Run microphone input and spoken output."""

        print("\nSnackStack Voice Mode is ready!")
        print("Speak clearly after each recording starts.")
        print("Say 'quit' or 'exit' to stop.")
        print("Say 'reset' to start a new conversation.\n")

        while True:
            question = self.recorder.listen()

            if not question:
                print("I couldn't understand that. Please try again.")
                continue

            command = question.lower().strip(" .!?")

            if command in ("quit", "exit", "stop"):
                farewell = "Goodbye! Thanks for using SnackStack."
                print(f"\nSnackStack: {farewell}")
                self.speaker.speak(farewell)
                break

            if command == "reset":
                self.reset()
                continue

            answer = self.ask(question)
            print(f"\nSnackStack: {answer}\n")
            self.speaker.speak(answer)


def main():
    parser = argparse.ArgumentParser(
        description="SnackStack food delivery assistant"
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--voice",
        action="store_true",
        help="Use microphone input and spoken output",
    )
    mode.add_argument(
        "--voice-out",
        action="store_true",
        help="Use typed input and spoken output",
    )

    args = parser.parse_args()

    assistant = SnackStackAssistant(
        voice_mode=args.voice,
        voice_out=args.voice_out,
    )

    if args.voice:
        assistant.voice_chat()
    else:
        assistant.chat()


if __name__ == "__main__":
    main()
