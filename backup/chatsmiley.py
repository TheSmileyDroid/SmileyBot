from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train based on the english corpus
trainer.train("chatterbot.corpus.portuguese")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.portuguese.greetings")

trainer.train("chatterbot.corpus.portuguese.conversations")

trainer.train("chatterbot.corpus.portuguese.compliment")

trainer.train("chatterbot.corpus.portuguese.linguistic_knowledge")

trainer.train("chatterbot.corpus.portuguese.proverbs")

trainer.train("chatterbot.corpus.portuguese.suggestions")


