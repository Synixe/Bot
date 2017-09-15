import discord
import json
import asyncio

CERT_FILE = "./data/certifications.json"
COURSE_FILE = "./data/courses.json"

class Commands():
    def register(self, _):

        return {
            "course" : {
                "function" : self.course,
                "description" : "Take a quick quiz to get a certification.",
                "roles" : ["@everyone"]
            },
            "cert" : {
                "function" : self.cert,
                "description" : "Display the certifications a user has.",
                "roles" : ["@everyone"]
            },
            "givecert" : {
                "function" : self.givecert,
                "description" : "Give a user a certification.",
                "roles" : ["manager"]
            },
            "remcert" : {
                "function" : self.remcert,
                "description" : "Remove a user's certification.",
                "roles" : ["manager"]
            }
        }

    async def course(self, data, client, message):
        certs = getCerts()
        if str(message.author.id) in certs:
            if data[0].lower() in certs[str(message.author.id)]:
                await message.channel.send(
                    "You already have that certification."
                )
                return
        courses = getCourses()
        if data[0].lower() not in courses:
            await message.channel.send(
                "That course does not exist."
            )
            return
        course = courses[data[0].lower()]
        del courses
        user = message.channel.guild.get_member(message.author.id)
        await user.send(course["name"])
        await user.send(course["description"])
        def question_check(m):
            return m.author == message.author
        correct = 0
        total = 0
        for step in course["steps"]:
            if "text" in step:
                await user.send(step["text"])
            if "question" and "answer" in step:
                total += 1
                await user.send(step["question"])
                try:
                    guess = await client.wait_for('message', check=question_check, timeout=60.0)
                    if guess.content.lower() == step["answer"].lower():
                        await user.send(":white_check_mark:")
                        correct += 1
                    else:
                        await user.send(":x:")
                        await user.send("The correct answer was "+step["answer"])
                except asyncio.TimeoutError:
                    await message.channel.send('Sorry, you took too long it was {}.'.format(step["answer"]))
                    return
        if total == correct:
            certs = getCerts()
            if str(user.id) not in certs:
                certs[str(user.id)] = [data[0].lower()]
            else:
                certs[str(user.id)].append(data[0].lower())
                await user.send("Congrats! You now have "+data[0].lower()+" certification! :thumbsup:")
            saveCerts(certs)
        else:
            await user.send("Sorry, you'll need to take this course again.")

    async def cert(self, data, client, message):
        certs = getCerts()
        if str(message.author.id) in certs:
            await message.channel.send(
                "You have the following certifications: " + (
                    ", ".join(certs[str(message.author.id)])
                )
            )
        else:
            await message.channel.send(
                "You do not have any certifications"
            )
        available = []
        if str(message.author.id) in certs:
            for cert in certs:
                if cert not in certs[str(message.author.id)]:
                    available.append(cert)
        else:
            available = certs
        if len(available) != 0:
            await message.channel.send(
                "Available Courses: " + (
                    ", ".join(available)
                )
            )

    async def givecert(self, data, client, message):
        try:
            user = message.channel.guild.get_member(int(data[0]))
        except:
            await message.channel.send("Unable to find that user.")
            return
        certs = getCerts()
        if str(user.id) not in certs:
            certs[str(user.id)] = [data[1].lower()]
        else:
            if data[1].lower() not in certs[str(user.id)]:
                certs[str(user.id)].append(data[1].lower())
                await user.send("Congrats! You now have "+data[1].lower()+" certification! :thumbsup:")
                await message.channel.send(user.name+" now has "+data[1].lower())
            else:
                await message.channel.send(user.name+" already has that certification.")
                return
        saveCerts(certs)

    async def remcert(self, data, client, message):
        try:
            user = message.channel.guild.get_member(int(data[0]))
        except:
            await message.channel.send("Unable to find that user.")
            return
        certs = getCerts()
        if str(user.id) not in certs:
            return
        else:
            if data[1].lower() in certs[str(user.id)]:
                certs[str(user.id)].remove(data[1].lower())
                await message.channel.send(user.name+" no longer has "+data[1].lower())
                saveCerts(certs)
            else:
                await message.channel.send(user.name+" does not have that certification.")

def getCerts():
    f = open(CERT_FILE)
    certs = json.loads(f.read())
    f.close()
    return certs

def saveCerts(certs):
    f = open(CERT_FILE,'w')
    f.write(json.dumps(certs, indent=4, sort_keys=True))
    f.close()

def getCourses():
    f = open(COURSE_FILE)
    courses = json.loads(f.read())
    f.close()
    return courses

def isQualified(id, requirements):
    if requirements == []:
        return True
    missing = []
    certs = getCerts()
    if str(id) not in certs:
        return requirements
    for q in requirements:
        if q not in certs[str(id)]:
            missing.append(q)
    if missing == []:
        return True
    else:
        return missing
