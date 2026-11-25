
from memory.memory_manager import MemoryManager

jarvis_memory = MemoryManager()

print("\n===== JARVIS MEMORY TEST =====")

# Save information
print(jarvis_memory.remember(
    "My name is Parasuraman"
))

print(jarvis_memory.remember(
    "I am developing a local AI assistant called JARVIS"
))

# Retrieve information
print("\nWhat I remember:")
print(jarvis_memory.recall())

# Search specific information
print("\nSearch result:")
print(jarvis_memory.recall("JARVIS"))

# Save conversation
jarvis_memory.remember_conversation(
    "What is my project name?",
    "Your project name is JARVIS."
)

# Retrieve previous conversations
print("\nRecent conversations:")
print(jarvis_memory.get_recent_conversations())

print("\n===== MEMORY TEST COMPLETED =====")
