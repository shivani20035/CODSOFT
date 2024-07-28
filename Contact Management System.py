import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")

        self.contacts = {}

        self.create_widgets()

    def create_widgets(self):
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Store Name:").grid(row=0, column=0, padx=5, pady=5)
        self.store_name_entry = tk.Entry(add_frame)
        self.store_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(add_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(add_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Address:").grid(row=3, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(add_frame)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(add_frame, text="Add Contact", command=self.add_contact).grid(row=4, columnspan=2, pady=10)

        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10)

        self.contact_listbox = tk.Listbox(list_frame, width=50)
        self.contact_listbox.grid(row=0, columnspan=2, padx=5, pady=5)
        self.contact_listbox.bind("<<ListboxSelect>>", self.display_contact_details)

        tk.Button(list_frame, text="View Contact List", command=self.view_contacts).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(list_frame, text="Search Contact", command=self.search_contact).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(list_frame, text="Update Contact", command=self.update_contact).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(list_frame, text="Delete Contact", command=self.delete_contact).grid(row=2, column=1, padx=5, pady=5)

        details_frame = tk.Frame(self.root)
        details_frame.pack(pady=10)

        self.details_text = tk.Text(details_frame, width=50, height=10, state='disabled')
        self.details_text.pack(pady=5)

    def add_contact(self):
        store_name = self.store_name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if store_name and phone_number:
            self.contacts[phone_number] = {
                'store_name': store_name,
                'phone_number': phone_number,
                'email': email,
                'address': address
            }
            messagebox.showinfo("Success", f"Contact '{store_name}' added successfully.")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Store name and phone number are required.")

    def view_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        for phone_number, info in self.contacts.items():
            self.contact_listbox.insert(tk.END, f"{info['store_name']} ({phone_number})")

    def search_contact(self):
        query = simpledialog.askstring("Search Contact", "Enter name or phone number to search:")
        if query:
            results = [info for info in self.contacts.values() if query in info['store_name'] or query in info['phone_number']]
            self.display_search_results(results)

    def display_search_results(self, results):
        self.contact_listbox.delete(0, tk.END)
        if results:
            for info in results:
                self.contact_listbox.insert(tk.END, f"{info['store_name']} ({info['phone_number']})")
        else:
            self.contact_listbox.insert(tk.END, "No contacts found.")

    def display_contact_details(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            contact_info = self.contact_listbox.get(selection[0])
            phone_number = contact_info.split('(')[1][:-1]
            info = self.contacts.get(phone_number)

            if info:
                details = (f"Store Name: {info['store_name']}\n"
                           f"Phone Number: {info['phone_number']}\n"
                           f"Email: {info['email']}\n"
                           f"Address: {info['address']}\n")
                self.details_text.config(state='normal')
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, details)
                self.details_text.config(state='disabled')

    def update_contact(self):
        selection = self.contact_listbox.curselection()
        if selection:
            contact_info = self.contact_listbox.get(selection[0])
            phone_number = contact_info.split('(')[1][:-1]
            info = self.contacts.get(phone_number)

            if info:
                store_name = simpledialog.askstring("Update Store Name", "Enter new store name:", initialvalue=info['store_name'])
                email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=info['email'])
                address = simpledialog.askstring("Update Address", "Enter new address:", initialvalue=info['address'])

                if store_name:
                    info['store_name'] = store_name
                if email:
                    info['email'] = email
                if address:
                    info['address'] = address

                self.contacts[phone_number] = info
                messagebox.showinfo("Success", f"Contact '{phone_number}' updated successfully.")
                self.view_contacts()

    def delete_contact(self):
        selection = self.contact_listbox.curselection()
        if selection:
            contact_info = self.contact_listbox.get(selection[0])
            phone_number = contact_info.split('(')[1][:-1]

            if phone_number in self.contacts:
                del self.contacts[phone_number]
                messagebox.showinfo("Success", f"Contact '{phone_number}' deleted successfully.")
                self.view_contacts()

    def clear_entries(self):
        self.store_name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

