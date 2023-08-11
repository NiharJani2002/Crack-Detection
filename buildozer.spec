[app]

# Title of your application
title = Crack Detection

# Package name
package.name = com.example.crackdetection

# Package domain (needed for android/ios packaging)
package.domain = org.test'

# Source code where the main.py lives
source.dir = .

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy

# Supported orientations
orientation = portrait

# Permissions (modify as needed)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Minimum Android API your app will support
android.minapi = 21

# Target Android API, should be as high as possible
android.api = 31

# List of Java .jar files to add to the libs
android.add_jars = path/to/your/library.jar

# List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# Full name including package path of the Java class that implements Android Activity
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-v8/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
# android.wakelock = False

# (str) Android additional adb arguments
# android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk


[buildozer]
log_level = 2
warn_on_root = 1
