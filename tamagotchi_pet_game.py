import random
import tkinter as tk
from tkinter import messagebox

# -------------------- PET CLASSES --------------------
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.energy = 50
        self.hunger = 50
        self.health = 100
        self.happiness = 50
        self.xp = 0
        self.level = 1

    def feed(self):
        food_energy = random.randint(5, 15)
        food_hunger = random.randint(5, 15)
        self.energy += food_energy
        self.hunger -= food_hunger
        if self.hunger < 0: self.hunger = 0
        self.random_event("feed")
        return f"{self.name} is eating 🍖 (+{food_energy} energy, -{food_hunger} hunger)"

    def play(self):
        if self.energy < 20:
            return f"{self.name} is too tired to play 😴"
        if self.hunger > 80:
            self.health -= 5
            return f"{self.name} is too hungry to play 🤢 (-5 health)"
        play_energy = random.randint(5, 15)
        play_hunger = random.randint(3, 10)
        happiness_gain = random.randint(5, 10)
        xp_gain = random.randint(5, 10)
        self.energy -= play_energy
        self.hunger += play_hunger
        self.happiness += happiness_gain
        self.xp += xp_gain
        self.level_up()
        self.random_event("play")
        return f"{self.name} played! 🎾 (-{play_energy} energy, +{play_hunger} hunger, +{happiness_gain} happiness, +{xp_gain} XP)"

    def sleep(self):
        sleep_energy = random.randint(10, 25)
        self.energy += sleep_energy
        if self.energy > 100: self.energy = 100
        self.random_event("sleep")
        return f"{self.name} is sleeping 🛌 (+{sleep_energy} energy)"

    def status(self):
        if self.hunger > 90:
            self.health -= 10
        if self.energy < 10:
            pass  # Extremely tired message optional
        return (f"Name: {self.name}\nAge: {self.age}\nLevel: {self.level}\nXP: {self.xp}\n"
                f"Energy: {self.energy}\nHunger: {self.hunger}\nHealth: {self.health}\nHappiness: {self.happiness}")

    def level_up(self):
        while self.xp >= 50:
            self.level += 1
            self.xp -= 50
            self.health += 10
            self.energy += 10
            self.happiness += 5

    def random_event(self, action):
        chance = random.randint(1, 100)
        if chance <= 20:
            event = random.choice(["toy", "sick", "energy_boost"])
            if event == "toy":
                self.happiness += 10
            elif event == "sick":
                self.health -= 10
            elif event == "energy_boost":
                self.energy += 15


class Dog(Pet):
    def play(self):
        msg = super().play()
        if self.energy >= 20 and self.hunger <= 80:
            msg += f"\n{self.name} says: Woof Woof! 🐶"
        return msg

class Cat(Pet):
    def play(self):
        msg = super().play()
        if self.energy >= 20 and self.hunger <= 80:
            msg += f"\n{self.name} says: Meow! 🐱"
        return msg

class Bird(Pet):
    def play(self):
        msg = super().play()
        if self.energy >= 20 and self.hunger <= 80:
            msg += f"\n{self.name} says: Tweet Tweet! 🐦"
        return msg

# -------------------- GUI APPLICATION --------------------
class PetGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Tamagotchi Multi-Pet Game 🐾")
        self.pets = []
        self.current_pet = None

        # Frames
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)
        self.middle_frame = tk.Frame(root)
        self.middle_frame.pack(pady=10)
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(pady=10)

        # Add Pet Widgets
        tk.Label(self.top_frame, text="Pet Name:").grid(row=0, column=0)
        self.pet_name_entry = tk.Entry(self.top_frame)
        self.pet_name_entry.grid(row=0, column=1)
        tk.Label(self.top_frame, text="Age:").grid(row=0, column=2)
        self.pet_age_entry = tk.Entry(self.top_frame)
        self.pet_age_entry.grid(row=0, column=3)
        tk.Label(self.top_frame, text="Type:").grid(row=0, column=4)
        self.pet_type_var = tk.StringVar(value="dog")
        tk.OptionMenu(self.top_frame, self.pet_type_var, "dog", "cat", "bird").grid(row=0, column=5)
        tk.Button(self.top_frame, text="Add Pet", command=self.add_pet).grid(row=0, column=6)

        # Pet Selection
        self.pet_listbox = tk.Listbox(self.middle_frame, width=30)
        self.pet_listbox.pack(side=tk.LEFT)
        self.pet_listbox.bind("<<ListboxSelect>>", self.select_pet)

        # Action Buttons
        self.action_text = tk.StringVar()
        tk.Button(self.middle_frame, text="Feed", command=self.feed_pet).pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.middle_frame, text="Play", command=self.play_pet).pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.middle_frame, text="Sleep", command=self.sleep_pet).pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.middle_frame, text="Show Status", command=self.show_status).pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.middle_frame, text="Leaderboard", command=self.show_leaderboard).pack(side=tk.TOP, fill=tk.X)

        # Message Display
        self.message_label = tk.Label(self.bottom_frame, textvariable=self.action_text, justify=tk.LEFT)
        self.message_label.pack()

    # -------------------- GUI METHODS --------------------
    def add_pet(self):
        name = self.pet_name_entry.get()
        age_text = self.pet_age_entry.get()
        pet_type = self.pet_type_var.get()
        if not name or not age_text.isdigit():
            messagebox.showerror("Error", "Please enter valid name and age")
            return
        age = int(age_text)
        if pet_type == "dog":
            pet = Dog(name, age)
        elif pet_type == "cat":
            pet = Cat(name, age)
        else:
            pet = Bird(name, age)
        self.pets.append(pet)
        self.pet_listbox.insert(tk.END, name)
        self.action_text.set(f"{name} added successfully! 🐾")
        self.pet_name_entry.delete(0, tk.END)
        self.pet_age_entry.delete(0, tk.END)

    def select_pet(self, event):
        selection = self.pet_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_pet = self.pets[index]
            self.action_text.set(f"Selected pet: {self.current_pet.name}")

    def feed_pet(self):
        if self.current_pet:
            self.action_text.set(self.current_pet.feed())

    def play_pet(self):
        if self.current_pet:
            self.action_text.set(self.current_pet.play())

    def sleep_pet(self):
        if self.current_pet:
            self.action_text.set(self.current_pet.sleep())

    def show_status(self):
        if self.current_pet:
            self.action_text.set(self.current_pet.status())

    def show_leaderboard(self):
        if not self.pets:
            self.action_text.set("No pets yet!")
            return
        leaderboard = sorted(self.pets, key=lambda x: x.level*10 + x.health + x.happiness, reverse=True)
        text = "🏆 Leaderboard 🏆\n"
        for idx, pet in enumerate(leaderboard, 1):
            text += f"{idx}. {pet.name} - Level: {pet.level}, Health: {pet.health}, Happiness: {pet.happiness}\n"
        self.action_text.set(text)

# -------------------- RUN APPLICATION --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PetGameGUI(root)
    root.mainloop()
