import OpenAI from "openai";

// getLocation
// getTravelTime
// getCurrentWeather
// Then pretrain
// Add more API's

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    dangerouslyAllowBrowser: true,
});


async function getLocation() {
    const response = await fetch('https://ipapi.co/json/');
    const locationData = await response.json();
    return locationData;
}

async function getCurrentWeather(latitude, longitude) {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=apparent_temperature`;
    const response = await fetch(url);
    const weatherData = await response.json();
    return weatherData;
}

async function getPTVInfo() {
    const PTVInfo = "The Public Transport Victoria (PTV) system is a comprehensive network of train, tram, and bus services operating in Victoria, Australia, especially in Melbourne. Trains, the backbone of Melbourne's public transport, connect suburbs to the city center. The city's iconic trams provide convenient inner-city travel, while buses cover areas less accessible by rail. Ticketing is managed via the myki card, a rechargeable smart card used across all modes of transport. Fares depend on travel zones and times, with options for daily caps and concessions. The system is accessible, featuring low-floor trams, tactile indicators, and equipped stations and stops. Operational hours for trains and trams extend to around midnight, with all-night services on weekends under the Night Network. Buses run on various schedules, often with reduced weekend services. PTV offers real-time information through displays, a journey planner, and a mobile app, aiding in travel planning and service updates. Safety is ensured through patrols, rules like myki validation, and CCTV surveillance. PTV emphasizes environmental sustainability by reducing emissions and promoting public transport to lessen road congestion. Continuous improvements and expansions are made to accommodate Melbourne's growing population, including infrastructure upgrades and new services. As a crucial part of Melbourne's urban dynamics, PTV is essential for commuters, students, tourists, and the public, known for its efficiency and coverage.";
    return PTVInfo;
}

const functionDefinitions = [
    {
        name: "getCurrentWeather",
        description: "Get the current weather in a given location given in latitude and longitude",
        parameters: {
            type: "object",
            properties: {
                latitude: {
                    type: "string",
                },
                longitude: {
                    type: "string",
                }
            },
            required: ["longitude", "latitude"]
        }
    },
    {
        name: "getLocation",
        description: "Get the user's location based on their IP address",
        parameters: {
            type: "object",
            properties: {}
        }
    }, 
    {
        name: "getPTVInfo",
        description: "Get specific information about the PTV system",
        parameters: {
            type: "object",
            properties: {}
        }
    }
]

const availableFunctions = {
    getCurrentWeather,
    getLocation,
    getPTVInfo
};

const messages = [{
    role: "system",
    content: `You are a helpful assistant. Only use the functions you have been provided with.`
}];

async function agent(userInput) {
    messages.push({
        role: "user",
        content: userInput,
    });
    
    for (let i = 0; i < 5; i++) {
        const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages: messages,
            functions: functionDefinitions
        });
            
        const { finish_reason, message } = response.choices[0];
        console.log(message);
        
        
        if (finish_reason === "function_call") {
            const functionName = message.function_call.name;           
            const functionToCall = availableFunctions[functionName];
            const functionArgs = JSON.parse(message.function_call.arguments);
            const functionArgsArr = Object.values(functionArgs);
            const functionResponse = await functionToCall.apply(null, functionArgsArr);
            
            messages.push({
                role: "function",
                name: functionName,
                content: `
                The result of the last function was this: ${JSON.stringify(functionResponse)}
                `
            });
        } 
        
        else if (finish_reason === "stop") {
            messages.push(message);
            return message.content;
        }
    }
    return "The maximum number of iterations has been met without a suitable answer. Please try again with a more specific input.";
}

export { agent };

agent("Please explain to me how I can get from my current location to the CBD, and whether I need to bring an umbrella.");