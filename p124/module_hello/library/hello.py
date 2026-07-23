#!/usr/bin/python3
#

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: hello
short_description: A demo module that prints a greeting message
version_added: "2.20"
description:
    - "A module that says hello."
options:
    name:
        description:
            - Name of the person to salute. If no value is provided the default
              value will be used.
        required: false
        type: str
        default: John Doe
author:
    - The Ops Team
"""

EXAMPLES = """
# Pass in a custom name
- name: Say hello to Linus Torvalds
  hello:
    name: "Linus Torvalds"
"""

RETURN = """
fact:
    description: Hello string
    type: str
    sample: Hello John Doe!
"""

from ansible.module_utils.basic import AnsibleModule

FACTS = "Hello {name}!"


def run_module():
    module_args = dict(
        name=dict(type="str", default="John Doe"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        fact="",
    )

    txt = FACTS.format(name=module.params["name"])
    print(txt)
    result["fact"] = txt
    if module.check_mode:
        return result
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
