import ctypes
import ctypes.wintypes
import threading

# Constants
FILE_LIST_DIRECTORY = 0x0001

FILE_NOTIFY_CHANGE_FILE_NAME = 0x00000001
FILE_NOTIFY_CHANGE_DIR_NAME = 0x00000002
FILE_NOTIFY_CHANGE_ATTRIBUTES = 0x00000004
FILE_NOTIFY_CHANGE_SIZE = 0x00000008
FILE_NOTIFY_CHANGE_LAST_WRITE = 0x00000010
FILE_NOTIFY_CHANGE_CREATION = 0x00000040

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

kernel32 = ctypes.windll.kernel32

class FILE_NOTIFY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('NextEntryOffset', ctypes.wintypes.DWORD),
        ('Action', ctypes.wintypes.DWORD),
        ('FileNameLength', ctypes.wintypes.DWORD),
        ('FileName', ctypes.c_wchar * 1024)  # Simplification
    ]

def watch_directory(path):
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004

    OPEN_EXISTING = 3
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

    handle = kernel32.CreateFileW(
        path,
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    if handle == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()

    buffer = ctypes.create_string_buffer(8192)
    bytes_returned = ctypes.wintypes.DWORD()

    print(f"Watching changes in: {path}")

    while True:
        success = kernel32.ReadDirectoryChangesW(
            handle,
            ctypes.byref(buffer),
            len(buffer),
            True,  # Watch subdirectories
            FILE_NOTIFY_CHANGE_FILE_NAME |
            FILE_NOTIFY_CHANGE_DIR_NAME |
            FILE_NOTIFY_CHANGE_ATTRIBUTES |
            FILE_NOTIFY_CHANGE_SIZE |
            FILE_NOTIFY_CHANGE_LAST_WRITE |
            FILE_NOTIFY_CHANGE_CREATION,
            ctypes.byref(bytes_returned),
            None,
            None
        )

        if not success:
            print("ReadDirectoryChangesW failed.")
            break

        offset = 0
        while offset < bytes_returned.value:
            info = ctypes.cast(
                ctypes.byref(buffer, offset),
                ctypes.POINTER(FILE_NOTIFY_INFORMATION)
            ).contents

            filename = ''.join(info.FileName[:info.FileNameLength // 2])
            action = info.Action

            actions = {
                1: "Created",
                2: "Deleted",
                3: "Modified",
                4: "Renamed (old name)",
                5: "Renamed (new name)"
            }

            print(f"Action: {actions.get(action, 'Unknown')} - {filename}")

            if info.NextEntryOffset == 0:
                break
            offset += info.NextEntryOffset

    kernel32.CloseHandle(handle)


if __name__ == "__main__":
    folder_to_watch = r"D:\Temp\log"  # Change this to the folder you want to monitor
    watch_thread = threading.Thread(target=watch_directory, args=(folder_to_watch,), daemon=True)
    watch_thread.start()

    try:
        # will block in 1s increments instead of burning CPU
        while watch_thread.is_alive():
            watch_thread.join(timeout=1)
        # watch_thread.join() # Ctrl+C’s not working will block until the thread is done
    except KeyboardInterrupt: # Ctrl+C’s
        print("Stopped monitoring.")

# prints:
# Action: Modified - log.txt
# Action: Created - New Text Document.txt
# Action: Renamed (old name) - New Text Document.txt
# Action: Renamed (new name) - log1.txt
# Action: Modified - log1.txt
