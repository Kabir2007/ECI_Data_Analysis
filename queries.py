# queries.py

SEARCH_QUERIES = [
    {
        "id": "district_voters",
        "description": "Number of voters by district (aggregate)",
        "queries": [
            "district wise electorate Election Commission",
            "electoral roll statistics district",
        ],
        "required_keywords": ["electors", "district", "roll"],
        "preferred_level": "district"
    },
    {
        "id": "form6_additions",
        "description": "Addition requests (Form 6) by constituency",
        "queries": [
            "Form 6 statistics Election Commission",
            "claims and objections electoral roll summary",
        ],
        "required_keywords": ["Form 6", "addition", "claims"],
        "preferred_level": "constituency"
    },
    {
        "id": "voter_migration",
        "description": "Voter migration / transposition data",
        "queries": [
            "Form 8A migration statistics",
            "electoral roll transposition report",
        ],
        "required_keywords": ["migration", "transposition"],
        "preferred_level": "aggregate"
    },
    {
        "id": "sir_2002",
        "description": "Special Intensive Revision 2002 data",
        "queries": [
            "Special Intensive Revision 2002 electoral roll",
            "SIR 2002 Election Commission report",
        ],
        "required_keywords": ["SIR", "2002", "revision"],
        "preferred_level": "historical"
    },
    {
        "id": "district_income",
        "description": "Per capita income by district",
        "queries": [
            "district per capita income India",
            "district domestic product India",
        ],
        "required_keywords": ["income", "district"],
        "preferred_level": "district"
    }
]
