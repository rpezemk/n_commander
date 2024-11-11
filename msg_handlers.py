def server_message_handler(address, *args):
    # keep line below for testing purpose
    # print(f"Received message at {address}: {args}")
    ...
    
    
    
msg_handlers = [("/*", server_message_handler)]