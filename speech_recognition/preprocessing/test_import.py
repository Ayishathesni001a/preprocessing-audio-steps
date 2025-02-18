# test.py
import pkg_resources
package = pkg_resources.working_set.by_key['praat-textgrids']
print(f"Package location: {package.location}")
print(f"Package details: {package}")