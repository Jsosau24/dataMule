from website import create_app, db

app = create_app()

@app.cli.command()
def initdb():
    """Initialize the database."""
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)