import webview

def main():
    webview.create_window("My Assembly IDE", "http://127.0.0.1:8000")
    webview.start(gui='gtk', debug=True)

if __name__ == '__main__':
    main()
