from website import create_app

app = create_app()

#rerun server when a change is made (only for development)
if __name__== "__main__":
    app.run(debug=True)
    
