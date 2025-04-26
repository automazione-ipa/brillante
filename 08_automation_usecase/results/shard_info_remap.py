from pydantic import BaseModel
from typing import Any

class ShardInfo(BaseModel):
    """For a large document, sharding may be performed to produce
    several document shards. Each document shard contains this field
    to detail which shard it is.

    Attributes:
        shard_index (int):
            The 0-based index of this shard.
        shard_count (int):
            Total number of shards.
        text_offset (int):
            The index of the first character in
            [Document.text][google.cloud.documentai.v1.Document.text] in
            the overall document global text.
    """

    shard_index: int
    shard_count: int
    text_offset: int
