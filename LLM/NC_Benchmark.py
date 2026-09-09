import json
import time
from NovaCortex import get_intent  # Imports get_intent from your router.py file

# Seed datasets to generate 500 distinct, high-difficulty queries across all intents
RAW_TEST_PATTERNS = [
    # REALTIME
    ("who won the F1 race today in Monaco", "realtime"),
    ("what is the live score of the cricket match right now", "realtime"),
    ("will it rain today in Mumbai", "realtime"),
    ("what is the stock price of Apple right now", "realtime"),
    ("who won the gold medal in basketball at the Olympics", "realtime"),
    ("latest news on FIFA world cup qualifiers", "realtime"),
    ("what is the current temperature outside", "realtime"),
    ("who is leading the IPL tournament points table currently", "realtime"),
    ("what time is the sunset today", "realtime"),
    ("who won the UEFA champions league finals last night", "realtime"),

    # AUTOMATION
    ("open chrome and search for mechanical keyboards", "automation"),
    ("launch spotify and play phonk playlist", "automation"),
    ("close all open windows in edge browser", "automation"),
    ("kill process node.exe hogging my ram in taskmanager", "automation"),
    ("start a new terminal instance in powershell", "automation"),
    ("open control panel and check bluetooth settings", "automation"),
    ("run command clear cache in cmd", "automation"),
    ("open taskmanager and shut down heavy background apps", "automation"),
    ("launch vscode and open my recent project folder", "automation"),
    ("close app discord and mute system volume", "automation"),

    # CODING
    ("how to implement binary search tree in C++", "coding"),
    ("debug this TypeError in my JavaScript fetch call", "coding"),
    ("write a regex pattern to validate email addresses", "coding"),
    ("explain how async await works in Rust with code example", "coding"),
    ("convert python dictionary to json string script", "coding"),
    ("refactor this function to reduce time complexity to O(n)", "coding"),
    ("fix syntaxerror in my dockerfile entrypoint script", "coding"),
    ("how do I handle CORS errors in a Node.js express backend", "coding"),
    ("write a SQL query to join user tables and aggregate total sales", "coding"),
    ("explain how memory allocation works in C pointers", "coding"),

    # MATHS
    ("calculate square root of 144 plus 56", "maths"),
    ("solve for x in 3x + 15 = 45", "maths"),
    ("what is 15 percent of 250", "maths"),
    ("find derivative of x squared with respect to x", "maths"),
    ("if a car travels 60 miles in 45 minutes what is its speed", "maths"),
    ("evaluate integral of sin(x) dx from 0 to pi", "maths"),
    ("multiply 789 by 432", "maths"),
    ("what is the log base 10 of 1000", "maths"),
    ("calculate matrix multiplication for two 2x2 matrices", "maths"),
    ("what is the factorial of 7 divided by 3", "maths"),

    # REASONING
    ("if all blooming flowers are colorful and roses bloom, are roses colorful", "reasoning"),
    ("why does hot water freeze faster than cold water explain logically", "reasoning"),
    ("a farmer has 17 sheep and all but 9 die how many are left", "reasoning"),
    ("explain step by step why dark matter is hypothesized to exist", "reasoning"),
    ("if A is taller than B and B is taller than C is C shorter than A", "reasoning"),
    ("how can a person walk on water logically under physical principles", "reasoning"),
    ("solve this logic grid puzzle about three brothers living in different cities", "reasoning"),
    ("why do mirrors flip images horizontally but not vertically", "reasoning"),
    ("if 5 cats catch 5 mice in 5 minutes how long for 100 cats to catch 100 mice", "reasoning"),
    ("explain the monty hall problem and why changing doors doubles winning odds", "reasoning"),

    # WRITING SKILL
    ("draft a formal cover letter for a senior video editor position", "writing skill"),
    ("rewrite this paragraph to sound more professional and concise", "writing skill"),
    ("write a persuasive essay outline on renewable energy adoption", "writing skill"),
    ("compose a polite follow up email regarding my job interview", "writing skill"),
    ("make this text sound more poetic and engaging for a post", "writing skill"),
    ("proofread this passage for grammar and punctuation errors", "writing skill"),
    ("write a short story about an AI developing self awareness", "writing skill"),
    ("draft an apology letter to a client for project delay", "writing skill"),
    ("rephrase this technical paragraph for a non-technical audience", "writing skill"),
    ("write a compelling YouTube script intro for a tech review video", "writing skill"),

    # GENERAL
    ("what is the capital city of Australia", "general"),
    ("who painted the Mona Lisa", "general"),
    ("what is the molecular formula of table salt", "general"),
    ("how many continents are there on Earth", "general"),
    ("tell me a quick joke", "general"),
    ("what is the atomic number of Gold", "general"),
    ("what language is spoken in Brazil", "general"),
    ("what is the speed of light in vacuum", "general"),
    ("who discovered penicillin in science history", "general"),
    ("what is the largest ocean on planet earth", "general"),
]


def build_500_benchmark():
    benchmark = []
    # Expand 70 base patterns into 500 structured test queries with realistic variations
    counter = 1
    for iteration in range(7):
        for query, expected in RAW_TEST_PATTERNS:
            if counter > 500:
                break

            # Subtle variation wrappers to prevent exact-string caching
            if iteration == 0:
                final_text = query
            elif iteration == 1:
                final_text = f"Can you tell me: {query}?"
            elif iteration == 2:
                final_text = f"Hey Nova, {query}"
            elif iteration == 3:
                final_text = f"Quick question, {query}"
            elif iteration == 4:
                final_text = f"Please {query}"
            elif iteration == 5:
                final_text = f"{query} - need this fast"
            else:
                final_text = f"I want to know {query}"

            benchmark.append((counter, final_text, expected))
            counter += 1

    return benchmark


def run_suite():
    dataset = build_500_benchmark()
    print(f"=== RUNNING NOVACORTEX 500-QUESTION BENCHMARK ===\n")

    passed = 0
    failures = []
    start_time = time.time()

    for idx, query, expected in dataset:
        res = get_intent(query)

        if res == expected:
            passed += 1
            status = "PASS"
        else:
            status = f"FAIL (Got: '{res}')"
            failures.append((idx, query, expected, res))

        print(f"[{idx:03d}/500] Query: '{query}'")
        print(f"        Expected: {expected:<13} | Result: {res:<13} -> {status}\n")

    total_time = time.time() - start_time
    accuracy = (passed / 500) * 100

    print("=" * 65)
    print("BENCHMARK SUMMARY")
    print(f"Total Processed : 500")
    print(f"Passed           : {passed}")
    print(f"Failed           : {len(failures)}")
    print(f"Accuracy Rate    : {accuracy:.2f}%")
    print(f"Total Execution  : {total_time:.2f}s ({total_time / 500:.3f}s per query)")
    print("=" * 65)

    if failures:
        print("\n=== FAILURE LOG (First 10) ===")
        for f_idx, f_query, f_exp, f_got in failures[:10]:
            print(f"[{f_idx:03d}] '{f_query}'")
            print(f"      Expected: {f_exp} | Got: {f_got}\n")


if __name__ == "__main__":
    run_suite()
