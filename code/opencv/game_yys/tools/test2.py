from pynput import keyboard

def f1():
    print "aaa"

def on_press(key):
    if key == keyboard.Key["f12"]:
        f1()
        return False

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
    listener.run()