import datetime

# Models
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.items = []
        self.bids = []

class Item:
    def __init__(self, name, description, min_price, end_time, seller):
        self.name = name
        self.description = description
        self.min_price = min_price
        self.highest_bid = None
        self.end_time = end_time
        self.seller = seller
        self.bids = []

class Bid:
    def __init__(self, user, amount):
        self.user = user
        self.amount = amount

# Online Auction System
class AuctionSystem:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None
        self.items = []

    # User registration
    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        self.users[username] = User(username, password)
        print("User registered successfully!")
        return True

    # User login
    def login_user(self, username, password):
        if username not in self.users or self.users[username].password != password:
            print("Invalid username or password.")
            return False
        self.logged_in_user = self.users[username]
        print(f"Welcome, {username}!")
        return True

    # User logout
    def logout(self):
        if self.logged_in_user:
            print(f"Goodbye, {self.logged_in_user.username}!")
            self.logged_in_user = None

    # Add item for auction
    def list_item(self, name, description, min_price, end_time):
        if not self.logged_in_user:
            print("Please log in to list an item.")
            return False

        try:
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            if end_time <= datetime.datetime.now():
                print("End time must be in the future.")
                return False
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD HH:MM:SS.")
            return False

        item = Item(name, description, min_price, end_time, self.logged_in_user)
        self.items.append(item)
        self.logged_in_user.items.append(item)
        print("Item listed successfully!")
        return True

    # Place a bid
    def place_bid(self, item_name, bid_amount):
        if not self.logged_in_user:
            print("Please log in to place a bid.")
            return False

        for item in self.items:
            if item.name == item_name:
                if datetime.datetime.now() > item.end_time:
                    print("Bidding has ended for this item.")
                    return False

                if bid_amount <= item.min_price:
                    print(f"Bid amount must be greater than the minimum price ({item.min_price}).")
                    return False

                if item.highest_bid and bid_amount <= item.highest_bid.amount:
                    print(f"Bid amount must be greater than the current highest bid ({item.highest_bid.amount}).")
                    return False

                bid = Bid(self.logged_in_user, bid_amount)
                item.bids.append(bid)
                item.highest_bid = bid
                self.logged_in_user.bids.append(bid)
                print("Bid placed successfully!")
                return True

        print("Item not found.")
        return False

    # Display active auctions
    def display_active_auctions(self):
        print("\nActive Auctions:")
        for item in self.items:
            if datetime.datetime.now() < item.end_time:
                print(f"Item: {item.name}, Description: {item.description}, "
                      f"Minimum Price: {item.min_price}, Ends: {item.end_time}, "
                      f"Current Highest Bid: {item.highest_bid.amount if item.highest_bid else 'None'}")
        print()

    # Display auction winners
    def display_winners(self):
        print("\nAuction Winners:")
        for item in self.items:
            if datetime.datetime.now() > item.end_time:
                if item.highest_bid:
                    print(f"Item: {item.name}, Winner: {item.highest_bid.user.username}, "
                          f"Winning Bid: {item.highest_bid.amount}")
                else:
                    print(f"Item: {item.name}, No bids placed.")
        print()

    # Search for items by name
    def search_items(self, keyword):
        print(f"\nSearch Results for '{keyword}':")
        found = False
        for item in self.items:
            if keyword.lower() in item.name.lower():
                found = True
                print(f"Item: {item.name}, Description: {item.description}, "
                      f"Minimum Price: {item.min_price}, Ends: {item.end_time}, "
                      f"Current Highest Bid: {item.highest_bid.amount if item.highest_bid else 'None'}")
        if not found:
            print("No items found.")
        print()

        # Delete an item listed by the seller
    def delete_item(self, item_name):
        if not self.logged_in_user:
            print("Please log in to delete an item.")
            return False

        for item in self.logged_in_user.items:
            if item.name == item_name:
                if item.bids:
                    print("Cannot delete this item. Bids have already been placed.")
                    return False
                self.items.remove(item)
                self.logged_in_user.items.remove(item)
                print("Item deleted successfully.")
                return True

        print("Item not found in your listings.")
        return False

        # Update minimum price for an item
    def update_min_price(self, item_name, new_min_price):
        if not self.logged_in_user:
            print("Please log in to update the minimum price.")
            return False

        for item in self.logged_in_user.items:
            if item.name == item_name:
                if item.bids:
                    print("Cannot update the minimum price. Bids have already been placed.")
                    return False
                item.min_price = new_min_price
                print("Minimum price updated successfully.")
                return True

        print("Item not found in your listings.")
        return False

        # View user profile
    def view_profile(self):
        if not self.logged_in_user:
            print("Please log in to view your profile.")
            return

        print(f"\nProfile of {self.logged_in_user.username}:")
        print("Listed Items:")
        for item in self.logged_in_user.items:
            print(f"- {item.name}, Minimum Price: {item.min_price}, Ends: {item.end_time}, "
                  f"Current Highest Bid: {item.highest_bid.amount if item.highest_bid else 'None'}")
        print("\nBids Placed:")
        for bid in self.logged_in_user.bids:
            print(f"- Item: {bid.user.username}, Bid Amount: {bid.amount}")
        print()

        # Report auction statistics
    def auction_statistics(self):
        total_items = len(self.items)
        total_bids = sum(len(item.bids) for item in self.items)
        avg_bids_per_item = total_bids / total_items if total_items > 0 else 0

        print("\nAuction Statistics:")
        print(f"Total Items Listed: {total_items}")
        print(f"Total Bids Placed: {total_bids}")
        print(f"Average Bids Per Item: {avg_bids_per_item:.2f}")
        print()

        # Check and close expired auctions
    def close_expired_auctions(self):
        now = datetime.datetime.now()
        for item in self.items:
            if now > item.end_time and not getattr(item, 'closed', False):
                setattr(item, 'closed', True)
                if item.highest_bid:
                    print(f"Auction Closed: {item.name} | Winner: {item.highest_bid.user.username} "
                          f"| Winning Bid: {item.highest_bid.amount}")
                else:
                    print(f"Auction Closed: {item.name} | No bids placed.")

        # Send a message to another user
    def send_message(self, recipient_username, message):
        if not self.logged_in_user:
            print("Please log in to send messages.")
            return False

        if recipient_username not in self.users:
            print("Recipient username not found.")
            return False

        recipient = self.users[recipient_username]
        if not hasattr(recipient, "messages"):
            recipient.messages = []

        recipient.messages.append((self.logged_in_user.username, message))
        print("Message sent successfully!")
        return True

    # View received messages
    def view_messages(self):
        if not self.logged_in_user:
            print("Please log in to view your messages.")
            return

        messages = getattr(self.logged_in_user, "messages", [])
        if not messages:
            print("No messages received.")
        else:
            print("\nMessages:")
            for sender, msg in messages:
                print(f"From {sender}: {msg}")
        print()

# Main Program
def main():
    auction_system = AuctionSystem()

    while True:
        print("\n=== Online Auction System ===")
        print("1. Register")
        print("2. Login")
        print("3. List an Item for Auction")
        print("4. Place a Bid")
        print("5. Display Active Auctions")
        print("6. Display Auction Winners")
        print("7. search_items")
        print("8. delete_item")
        print("9. update_min_price")
        print("10. view_profile")
        print("11. auction_statistics")
        print("12. send_message")
        print("13. view_messages")
        print("14. Close auctions")
        print("15. logout")
        print("16. exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            auction_system.register_user(username, password)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            auction_system.login_user(username, password)

        elif choice == "3":
            name = input("Enter item name: ")
            description = input("Enter item description: ")
            min_price = float(input("Enter minimum price: "))
            end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
            auction_system.list_item(name, description, min_price, end_time)

        elif choice == "4":
            item_name = input("Enter item name: ")
            bid_amount = float(input("Enter your bid amount: "))
            auction_system.place_bid(item_name, bid_amount)

        elif choice == "5":
            auction_system.display_active_auctions()

        elif choice == "6":
            auction_system.display_winners()

        elif choice == "7":
            keyword = input("Enter keyword to search: ")
            auction_system.search_items(keyword)

        elif choice == "8":
            keyword = input("Enter keyword to delete: ")
            auction_system.delete_item(keyword)
        
        elif choice == "9":
            item_name = input("Enter item name: ")
            new_min_price = float(input("Enter new minimum price: "))
            auction_system.update_min_price(item_name, new_min_price)
        
        elif choice == "10":
            auction_system.view_profile()

        elif choice == "11":
            auction_system.auction_statistics()
        
        elif choice == "12":
            auction_system.send_message()
        
        elif choice == "13":
            auction_system.view_messages()
        
        elif choice == "14":
            auction_system.close_expired_auctions()
    
        elif choice == "15":
            auction_system.logout()

        elif choice == "16":
            print("Thank you for using the Online Auction System!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
