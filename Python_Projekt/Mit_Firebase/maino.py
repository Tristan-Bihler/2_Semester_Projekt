import Shop
import Kunde

auth = False

if __name__ == "__main__":
    user = Kunde.Kunde()
    Shop_ui = Shop.Main_Window(user)

    Shop_ui.mainloop()