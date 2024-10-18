
"use client";

import { useState } from "react";
import { useModelService } from "../services/modelService";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function ModelUI() {
  const { response, queryModel } = useModelService();
  const [query, setQuery] = useState("");

  const handleQuery = () => {
    queryModel(query);
    setQuery("");
  };

  return (
    <Card className="w-full max-w-md mx-auto mt-10">
      <CardHeader>
        <CardTitle>AI Model Interface</CardTitle>
      </CardHeader>
      <CardContent>
        <Input
          type="text"
          placeholder="Enter your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="mt-4">
          <Button onClick={handleQuery}>Submit</Button>
        </div>
        {response && (
          <div className="mt-4 p-4 bg-gray-100 rounded">
            <strong>Response:</strong> {response}
          </div>
        )}
      </CardContent>
      <CardFooter>
        <p className="text-sm text-gray-500">Powered by Custom AI Model</p>
      </CardFooter>
    </Card>
  );
}
