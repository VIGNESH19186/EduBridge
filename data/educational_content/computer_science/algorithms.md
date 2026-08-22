# Computer Science - Algorithms & Control Flow

## Section: Loops and Time Complexity

A single for-loop that iterates over n items has a time complexity of O(n),
meaning the time it takes grows linearly with the size of the input. This is
because the loop body executes exactly n times, each taking constant time
(assuming the operations inside the loop are O(1)).

## Section: Nested Loops

A nested loop, where one loop runs inside another, typically has a time
complexity of O(n^2) if both loops iterate over the same n items, since the
inner loop executes n times for every single iteration of the outer loop.

## Section: Common Mistakes

A common mistake is assuming all loops are O(n) regardless of nesting, or
forgetting that operations inside the loop (like another loop, or a sort) can
increase the overall complexity beyond a simple linear count.
