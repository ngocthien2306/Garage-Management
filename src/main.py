import os

import click
import uvicorn



def main():
    uvicorn.run(
        app="app.server:app",
        reload=True,
        workers=1,
        port=8001
    )


if __name__ == "__main__":
    main()