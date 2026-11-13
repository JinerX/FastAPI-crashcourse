from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

message = """
He quickly dismissed my notion that he himself was ill, though he did want to discuss a specific disease.
"Vampirism," he said, and then paused at my quizzical look. "I was told that you were someone I should seek out for help understanding it."
"Who told you that?" I asked with a smile.
"Tissina Gray."
I immediately remembered her. A brave, beautiful knight who had needed my assistance separating fact from fiction on the subject of the vampire. It had been two years, and I had never heard whether my advice had proved effective.
"You've spoken to her? How is her ladyship?" I asked.
"Dead," Movarth replied coldly, and then, responding to my shock, he added to perhaps soften the blow. "She said your advice was invaluable, at least for the one vampire. When last I talked to her, she was tracking another. It killed her."
"Then the advice I gave her was not enough," I sighed. "Why do you think it would be enough for you?"
"I was a teacher once myself, years ago," he said. "Not in a university. A trainer in the Fighters Guild. But I know that if a student doesn't ask the right questions, the teacher cannot be responsible for his failure. I intend to ask you the right questions."
And that he did. For hours, he asked questions and I answered what I could, but he never volunteered any information about himself. He never smiled. He only studied me with those intense eyes of his, commiting [sic] every word I said to memory.
Finally, I turned the questioning around. "You said you were a trainer at the Fighters Guild. Are you on an assignment for them?"
"No," he said curtly, and finally I could detect some weariness in those feverish eyes of his. "I would like to continue this tomorrow night, if I could. I need to get some sleep and absorb this."
"You sleep during the day," I smiled.
To my surprise, he returned the smile, though it was more of a grimace. "When tracking your prey, you adapt their habits."
The next day, he did return with more questions, these ones very specific. He wanted to know about the vampires of eastern Skyrim. I told him about the most powerful tribe, the Volkihar, paranoid and cruel, whose very breath could freeze their victims' blood in the veins. I explained to him how they lived beneath the ice of remote and haunted lakes, never venturing into the world of men except to feed.
From UESP Immortal Bloos
"""

@app.get("/story/stream", response_class=StreamingResponse) # 
async def get_stream() -> AsyncIterable[str]:
    for line in message:
        yield line
